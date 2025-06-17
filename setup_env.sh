#!/bin/bash

echo "Mise à jour des paquets système..."
sudo apt update

echo "Installation des dépendances système (espeak, mbrola, pip)..."
sudo apt install -y espeak mbrola mbrola-fr1 python3-pip

echo "Création d'un environnement Python virtuel (./venv)..."
python3 -m venv venv

echo "Activation de l'environnement virtuel..."
source venv/bin/activate

echo "Installation des bibliothèques Python requises..."
pip install --upgrade pip
pip install -r raspberry-pi/requirements.txt

echo "Environnement prêt !"
echo
echo "Pour lancer l'assistant vocal, exécute :"
echo "    source venv/bin/activate"
echo "    python3 raspberry-pi/main.py"
echo
echo "Pour quitter l'environnement virtuel :"
echo "    deactivate"
