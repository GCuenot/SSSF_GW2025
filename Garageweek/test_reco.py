import serial
import sounddevice as sd
import queue
import vosk
import sys
import json

# Charger le modèle Vosk
model = vosk.Model("model")  # dossier modèle Vosk
samplerate = 16000

# File d'attente audio
q = queue.Queue()

# Ouverture du port série (remplace par le bon port COM ou /dev)
arduino = serial.Serial('COM5', 9600)  # Exemple : '/dev/ttyUSB0' sur Linux

# Callback d’entrée audio
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Démarrer l’écoute
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

            if "étape suivante" in texte:
                print("Commande : NEXT")
                arduino.write(b'next\n')

            elif "étape précédente" in texte:
                print("Commande : PREV")
                arduino.write(b'prev\n')
