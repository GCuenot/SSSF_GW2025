# Cooking Assistant Project

## Overview
The Cooking Assistant project is designed to help users follow cooking steps using voice commands. It integrates an Arduino Uno R3 with an LCD display to show the current cooking step and a Raspberry Pi 4B that handles voice recognition and serial communication with the Arduino.

## Components
The project consists of two main components:

1. **Arduino Component**:
   - **cooking_steps.ino**: This Arduino sketch manages the cooking steps, initializes the LCD display, and handles serial commands to navigate through the steps.

2. **Raspberry Pi Component**:
   - **main.py**: The main entry point for the Raspberry Pi application. It initializes serial communication and voice recognition, listens for voice commands, and sends commands to the Arduino while providing audio feedback.
   - **voice_recognition.py**: Handles voice recognition using the Vosk library, capturing audio input and recognizing specific commands related to cooking steps.
   - **serial_comm.py**: Defines a class `SerialComm` that manages serial communication with the Arduino, including methods to connect, send commands, read responses, and close the connection.
   - **requirements.txt**: Lists the required Python libraries for the Raspberry Pi application, including `vosk`, `sounddevice`, and `pyserial`.

## Setup Instructions

### Arduino Setup
1. Connect the Arduino Uno R3 to your computer via USB.
2. Open the Arduino IDE and load the `cooking_steps.ino` sketch.
3. Upload the sketch to the Arduino.
4. Connect an LCD display to the Arduino as specified in the sketch.

### Raspberry Pi Setup
1. Ensure your Raspberry Pi is set up with an appropriate operating system.
2. Install the required Python libraries by running:
   ```
   pip install -r requirements.txt
   ```
3. Connect the Arduino to the Raspberry Pi via USB.
4. Run the `main.py` script to start the Cooking Assistant.

## Usage
Once everything is set up, you can use voice commands such as "étape suivante" (next step), "étape précédente" (previous step), and "répéter" (repeat) to navigate through the cooking steps. The current step will be displayed on the Arduino's LCD, and the Raspberry Pi will provide audio feedback using the `espeak` command.

## License
This project is open-source and available for modification and distribution under the MIT License.

faut faire ça btw
sudo apt install espeak mbrola mbrola-fr1
