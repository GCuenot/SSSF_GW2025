import serial
import sounddevice as sd
import queue
import vosk
import sys
import json
import subprocess
import difflib
import unicodedata
from threading import Thread

# --- Chargement des recettes ---
with open("recettes.json", "r") as f:
    recettes_data = json.load(f)

# --- Outils utiles ---
def nettoyer_texte(txt):
    txt = txt.lower()
    txt = unicodedata.normalize('NFD', txt).encode('ascii', 'ignore').decode('utf-8')
    return txt

def is_similar(a, b, threshold=0.7):
    return difflib.SequenceMatcher(None, a, b).ratio() >= threshold

# --- Recette par défaut
recette = recettes_data["recettes"][0]
titre = recette["titre"]
description = recette["description"]
etapes = recette["etapes"]
current_index = 0

print(f"Recette selectionnée : {titre}")
print(f"Description : {description}")

def envoyer_etape(index):
    texte = f"Etape {index + 1}/{len(etapes)}: {etapes[index]}"
    arduino.write((texte + '\n').encode())
    subprocess.run(['espeak', '-v', 'mb-fr1', '-s','140', '-p','50', '-a', '200', etapes[index]])
    return etapes[index]

def ecoute_arduino():
    global current_index
    while True:
        if arduino.in_waiting:
            ligne = arduino.readline().decode().strip()
            print("Arduino a envoyé :", ligne)
            if ligne == "next":
                current_index = min(current_index + 1, len(etapes) - 1)
                envoyer_etape(current_index)

# --- Initialisation ---
model = vosk.Model("model")
samplerate = 16000
q = queue.Queue()
arduino = serial.Serial('/dev/ttyACM0', 9600)

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

last_cmd = None
last_msg = None
Thread(target=ecoute_arduino, daemon=True).start()

# --- Boucle d'écoute ---
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, samplerate)
    print("Parlez :")

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            texte = result.get("text", "").lower()
            print("Texte détecté :", texte)

            # Lecture de la liste des recettes
            if "quelles sont les recettes" in texte or "liste des recettes" in texte:
                titres = [r["titre"] for r in recettes_data["recettes"]]
                liste = ", ".join(titres)
                print("Recettes disponibles :", liste)
                subprocess.run(['espeak', '-v', 'mb-fr1', '-s','140', '-p','50', '-a', '200', 'Les recettes disponibles sont : ' + liste])
                continue

            # Détection de recette dans la phrase
            for r in recettes_data["recettes"]:
                titre_nettoye = nettoyer_texte(r["titre"])
                if titre_nettoye in nettoyer_texte(texte):
                    recette = r
                    titre = recette["titre"]
                    description = recette["description"]
                    etapes = recette["etapes"]
                    current_index = 0
                    print(f"Nouvelle recette : {titre}")
                    subprocess.run(['espeak', '-v', 'mb-fr1', '-s','140', '-p','50', '-a', '200', f"Recette {titre} sélectionnée"])
                    envoyer_etape(current_index)
                    break

            # Navigation classique
            if is_similar(texte, "étape suivante"):
                current_index = min(current_index + 1, len(etapes) - 1)
                print("Commande : NEXT")
                last_cmd = b'next\n'
                last_msg = envoyer_etape(current_index)

            elif is_similar(texte, "étape précèdente"):
                current_index = max(current_index - 1, 0)
                print("Commande : PREV")
                last_cmd = b'prev\n'
                last_msg = envoyer_etape(current_index)

            elif is_similar(texte, "recommencer"):
                current_index = 0
                print("Commande : RESTART")
                last_cmd = b'start\n'
                last_msg = envoyer_etape(current_index)

            elif any(is_similar(texte, cmd) for cmd in ["répète", "répèter", "répètez","répètition", "recommencer la commande", "recommencer la dernière commande", "recommencer la dernière étape"]):
                if last_cmd and last_msg:
                    print("Commande : REPEAT")
                    arduino.write((last_msg + '\n').encode())
                    subprocess.run(['espeak', '-v', 'mb-fr1', '-s','140', '-p','50', '-a', '200', last_msg])
                else:
                    print("Aucune commande précédente a répéter.")
c