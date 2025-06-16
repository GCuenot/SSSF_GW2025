# Cooking Assistant Project

## Overview
The Cooking Assistant project is designed to help users follow cooking steps using voice commands. It consists of two main components: an Arduino-based system that displays cooking steps on an LCD and a Raspberry Pi application that handles voice recognition and communicates with the Arduino.

## Project Structure
```
cooking-assistant
├── arduino
│   ├── cooking_steps.ino       # Arduino sketch for managing cooking steps
│   └── README.md               # Documentation for the Arduino component
├── raspberry-pi
│   ├── main.py                 # Main entry point for the Raspberry Pi application
│   ├── voice_recognition.py     # Handles voice recognition
│   ├── serial_comm.py           # Manages serial communication with Arduino
│   ├── requirements.txt         # Lists required Python libraries
│   └── README.md                # Documentation for the Raspberry Pi component
└── README.md                    # Main documentation for the entire project
```

## Components

### Arduino
- **cooking_steps.ino**: This file contains the Arduino sketch that initializes an LCD display, defines cooking steps, and handles serial commands to navigate through the steps.

### Raspberry Pi
- **main.py**: The main entry point for the Raspberry Pi application. It initializes serial communication and voice recognition, listens for voice commands, and sends commands to the Arduino while providing audio feedback.
- **voice_recognition.py**: This file handles voice recognition using the Vosk library. It captures audio input, processes it, and recognizes specific commands related to cooking steps.
- **serial_comm.py**: Defines a class `SerialComm` that manages serial communication with the Arduino. It includes methods to connect, send commands, read responses, and close the connection.
- **requirements.txt**: Lists the required Python libraries for the Raspberry Pi application, including `vosk`, `sounddevice`, and `pyserial`.

## Getting Started
1. **Arduino Setup**:
   - Connect the Arduino to your computer.
   - Open the `cooking_steps.ino` file in the Arduino IDE.
   - Upload the sketch to the Arduino.

2. **Raspberry Pi Setup**:
   - Install the required Python libraries listed in `requirements.txt` using pip.
   - Connect the Arduino to the Raspberry Pi via USB.
   - Run the `main.py` script to start the voice recognition and cooking assistant.

## Usage
- Use voice commands such as "étape suivante" (next step) and "étape précédente" (previous step) to navigate through the cooking steps.
- The current step will be displayed on the Arduino's LCD and read aloud using the Raspberry Pi's audio output.

## Conclusion
This project combines hardware and software to create an interactive cooking assistant that enhances the cooking experience through voice commands and visual feedback.