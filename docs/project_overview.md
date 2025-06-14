# Project Overview

## Project Title: Arduino Voice Cooking Assistant

### Overview
The Arduino Voice Cooking Assistant is an interactive cooking guide that utilizes voice recognition technology to navigate through cooking steps. The project integrates an Arduino Nano with an LCD display and a Raspberry Pi 4B to create a seamless cooking experience. Users can verbally command the assistant to move to the next or previous cooking step, which will be displayed on the LCD and read aloud using text-to-speech functionality.

### Objectives
- To provide an intuitive cooking assistant that responds to voice commands.
- To display the current cooking step on an LCD connected to the Arduino.
- To read the cooking step aloud using the Raspberry Pi's text-to-speech capabilities.
- To facilitate a hands-free cooking experience, allowing users to focus on their cooking tasks.

### Components
1. **Arduino Nano**: Manages the LCD display and handles serial communication with the Raspberry Pi.
   - **cooking_steps.ino**: The Arduino sketch that displays the current cooking step and responds to commands from the Raspberry Pi.

2. **Raspberry Pi 4B**: Acts as the main processing unit for voice recognition and command handling.
   - **main.py**: The main entry point for the Raspberry Pi application, initializing voice recognition and managing interactions with the Arduino.
   - **voice_recognition.py**: Implements voice recognition functionality to listen for commands.
   - **serial_comm.py**: Manages serial communication with the Arduino, sending commands based on recognized voice input.
   - **requirements.txt**: Lists the necessary Python dependencies for the Raspberry Pi application.

### Interaction Flow
1. The user speaks a command (e.g., "next step" or "previous step").
2. The Raspberry Pi captures the audio and processes it using voice recognition.
3. Based on the recognized command, the Raspberry Pi sends a corresponding command to the Arduino via serial communication.
4. The Arduino receives the command, updates the LCD display with the current cooking step, and can also trigger audio playback on the Raspberry Pi to read the step aloud.

### Conclusion
This project aims to enhance the cooking experience by combining voice recognition technology with a user-friendly interface. By integrating the Arduino and Raspberry Pi, the assistant provides real-time feedback and guidance, making cooking more accessible and enjoyable.