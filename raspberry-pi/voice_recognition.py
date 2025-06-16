import serial
import sounddevice as sd
import queue
import vosk
import sys
import json
import subprocess
import difflib
from threading import Thread

# --- Chargement des recettes ---
with open("recettes.json", "r") as f:
    data = json.load(f)

# Choisir une recette (la première pour l'instant)
recette = data["recettes"][0]
titre = recette["titre"]
description = recette["description"]
etapes = recette["etapes"]

print(f"Recette selectionnee : {titre}")
print(f"Description : {description}")

# --- Outils utiles ---
def is_similar(a, b, threshold=0.7):
    return difflib.SequenceMatcher(None, a, b).ratio() >= threshold

current_index = 0

def envoyer_etape(index):
    texte = f"Etape {index + 1}/{len(etapes)}: {etapes[index]}"
    arduino.write((texte + '\n').encode())
    subprocess.run(['espeak', '-v', 'fr-fr', etapes[index]])
    return etapes[index]

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

def ecoute_arduino():
    global index
    while True:
        if arduino.in_waiting:
            ligne = arduino.readline().decode().strip()
            print("Arduino a envoyé :", ligne)
            if ligne == "next":
                index = min(index + 1, len(etapes) - 1)
                envoyer_etape(index)