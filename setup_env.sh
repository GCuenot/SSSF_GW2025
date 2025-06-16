#!/bin/bash

echo "Création de l'environnement virtuel Python..."
python3 -m venv venv

echo "Environnement créé dans ./venv"

echo "Activation de l'environnement..."
source venv/bin/activate

echo "Installation des dépendances depuis requirements.txt..."
pip install --upgrade pip
pip install -r raspberry-pi/requirements.txt

echo "Installation terminée."

echo "Pour lancer le programme, exécute :"
echo "    source venv/bin/activate"
echo "    python raspberry-pi/main.py"

echo "Pour quitter l'environnement virtuel :"
echo "    deactivate"
