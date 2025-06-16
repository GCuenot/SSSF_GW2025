import difflib

# ...

COMMANDS = {
    "étape suivante": ("next\n", "Étape suivante"),
    "étape précédente": ("prev\n", "Étape précédente"),
    "répète": (None, None),  # handled separately
    "répéter": (None, None), # handled separately
}

def find_best_command(texte):
    best_match = None
    highest = 0.0
    for cmd in COMMANDS:
        ratio = difflib.SequenceMatcher(None, texte, cmd).ratio()
        if ratio > highest:
            highest = ratio
            best_match = cmd
    return best_match if highest > 0.7 else None  # seuil à ajuster

# ...

while True:
    data = q.get()
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        texte = result.get("text", "").lower()
        print("Texte détecté :", texte)

        cmd = find_best_command(texte)
        if cmd == "étape suivante":
            print("Commande : NEXT")
            arduino.write(b'next\n')
            subprocess.run(['espeak', '-v', 'fr-fr', 'Étape suivante'])
            last_cmd = b'next\n'
            last_msg = 'Étape suivante'

        elif cmd == "étape précédente":
            print("Commande : PREV")
            arduino.write(b'prev\n')
            subprocess.run(['espeak', '-v', 'fr-fr', 'Étape précédente'])
            last_cmd = b'prev\n'
            last_msg = 'Étape précédente'

        elif cmd in ("répète", "répéter"):
            if last_cmd and last_msg:
                print("Commande : REPEAT")
                arduino.write(last_cmd)
                subprocess.run(['espeak', '-v', 'fr-fr', last_msg])
            else:
                print("Aucune commande précédente à répéter.")
