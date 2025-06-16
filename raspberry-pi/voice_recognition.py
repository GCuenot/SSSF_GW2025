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
    data = json.load(f)

# --- Outils utiles ---
def nettoyer_texte(txt):
    txt = txt.lower()
    txt = unicodedata.normalize('NFD', txt).encode('ascii', 'ignore').decode('utf-8')
    return txt

def is_similar(a, b, threshold=0.7):
    return difflib.SequenceMatcher(None, a, b).ratio() >= threshold

def choisir_recette_depuis_texte(texte_utilisateur):
    texte_nettoye = nettoyer_texte(texte_utilisateur)
    for recette in data["recettes"]:
        titre_nettoye = nettoyer_texte(recette["titre"])
        if is_similar(texte_nettoye, titre_nettoye):
            return recette
    return None

# --- Recette par défaut
recette = data["recettes"][0]
titre = recette["titre"]
description = recette["description"]
etapes = recette["etapes"]
current_index = 0

print(f"Recette selectionnee : {titre}")
print(f"Description : {description}")

def envoyer_etape(index):
    texte = f"Etape {index + 1}/{len(etapes)}: {etapes[index]}"
    arduino.write((texte + '\n').encode())
    subprocess.run(['espeak', '-v', 'fr-fr', etapes[index]])
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
            print("Texte detecte :", texte)

            # 🎯 Choix de recette par la voix
            selection = choisir_recette_depuis_texte(texte)
            if selection:
                recette = selection
                titre = recette["titre"]
                description = recette["description"]
                etapes = recette["etapes"]
                current_index = 0
                print(f"Nouvelle recette : {titre}")
                subprocess.run(['espeak', '-v', 'fr-fr', f"Recette {titre} selectionnee"])
                envoyer_etape(current_index)
                continue

            # 📖 Navigation classique
            if is_similar(texte, "etape suivante"):
                current_index = min(current_index + 1, len(etapes) - 1)
                print("Commande : NEXT")
                last_cmd = b'next\n'
                last_msg = envoyer_etape(current_index)

            elif is_similar(texte, "etape precedente"):
                current_index = max(current_index - 1, 0)
                print("Commande : PREV")
                last_cmd = b'prev\n'
                last_msg = envoyer_etape(current_index)

            elif is_similar(texte, "recommencer"):
                current_index = 0
                print("Commande : RESTART")
                last_cmd = b'start\n'
                last_msg = envoyer_etape(current_index)

            elif any(is_similar(texte, cmd) for cmd in ["repete", "repeter"]):
                if last_cmd and last_msg:
                    print("Commande : REPEAT")
                    arduino.write((last_msg + '\n').encode())
                    subprocess.run(['espeak', '-v', 'fr-fr', last_msg])
                else:
                    print("Aucune commande precedente a repeter.")
