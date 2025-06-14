import serial
import sounddevice as sd
import queue
import vosk
import sys
import json
import subprocess

# Charger le modèle Vosk
model = vosk.Model("model")  # dossier modèle Vosk
samplerate = 16000

# File d'attente audio
q = queue.Queue()

# Ouverture du port série
arduino = serial.Serial('/dev/ttyACM0', 9600)  # Modifier selon le port de l'Arduino

# Callback d’entrée audio
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

last_cmd = None
last_msg = None

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
                subprocess.run(['espeak', 'Étape suivante'])
                last_cmd = b'next\n'
                last_msg = 'Étape suivante'

            elif "étape précédente" in texte:
                print("Commande : PREV")
                arduino.write(b'prev\n')
                subprocess.run(['espeak', 'Étape précédente'])
                last_cmd = b'prev\n'
                last_msg = 'Étape précédente'

            elif "répète" in texte or "répéter" in texte:
                if last_cmd and last_msg:
                    print("Commande : REPEAT")
                    arduino.write(last_cmd)
                    subprocess.run(['espeak', last_msg])
                else:
                    print("Aucune commande précédente à répéter.")