# Cooking Assistant

Un assistant vocal embarqué pour la cuisine, combinant une **Raspberry Pi 4B**, un **Arduino Uno R3** et un **écran LCD** pour guider pas à pas une recette avec la voix... ou un geste !

---

## Fonctionnalités

- Reconnaissance vocale offline avec [Vosk](https://alphacephei.com/vosk/)
- Synthèse vocale en français avec `espeak`
- Affichage de l'étape courante sur écran LCD (via Arduino)
- Sélection vocale de la recette (ex. : "je veux faire un gratin dauphinois")
- Commandes vocales :
  - `étape suivante`
  - `étape précédente`
  - `répète`
  - `recommencer`
  - `quelles sont les recettes`
- Support du capteur de proximité : geste = étape suivante
- Recettes en JSON éditables, avec dernière étape automatique ("Bon appétit !")

---

## Composants

### Arduino
- `cooking_steps.ino` : gère l'écran LCD, reçoit les textes à afficher depuis la Pi

### Raspberry Pi
- `main.py` : point d'entrée principal
- `voice_recognition.py` : gestion complète de la voix, des recettes, et des interactions
- `recettes.json` : toutes les recettes avec étapes
- `requirements.txt` : dépendances Python (`vosk`, `sounddevice`, `pyserial`)

---

## Installation

### Pré-requis
```bash
sudo apt update
sudo apt install espeak mbrola mbrola-fr1 python3-pip
```

### Dépendances Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r raspberry-pi/requirements.txt
```

### Arduino
1. Brancher l’Arduino Uno à l'écran LCD (I2C, 4 fils)
2. Flasher `arduino/cooking_steps/cooking_steps.ino` depuis l’IDE Arduino
3. Laisser l’Arduino branché à la Raspberry Pi en USB

---

## Utilisation

### Lancer l’assistant :
```bash
cd SSSF_GW2025
source venv/bin/activate
python3 raspberry-pi/main.py
```

### Commandes vocales :
- `"je veux faire un poulet curry coco"`
- `"étape suivante"`
- `"répète"`
- `"quelles sont les recettes"`

> Le programme lit et affiche chaque étape de la recette.  
> À la fin, il vous dit `"La recette est terminée. Bon appétit !"`
