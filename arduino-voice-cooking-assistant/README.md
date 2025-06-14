# Arduino Voice Cooking Assistant

This project is designed to facilitate cooking by providing voice recognition capabilities to navigate through cooking steps. It consists of two main components: an Arduino Nano that manages the display of cooking steps on an LCD and a Raspberry Pi that handles voice recognition and communication with the Arduino.

## Project Structure

- **arduino/**
  - **cooking_steps.ino**: Arduino sketch for managing the LCD display and serial communication.
  - **README.md**: Documentation for the Arduino component.

- **raspberry-pi/**
  - **main.py**: Main entry point for the Raspberry Pi application.
  - **requirements.txt**: Python dependencies for the Raspberry Pi application.
  - **voice_recognition.py**: Implementation of voice recognition functionality.
  - **serial_comm.py**: Handles serial communication with the Arduino.
  - **README.md**: Documentation for the Raspberry Pi component.

- **docs/**
  - **project_overview.md**: Overview of the project and its components.

## Setup Instructions

### Arduino Setup
1. Connect the Arduino Nano to your computer.
2. Upload the `cooking_steps.ino` sketch to the Arduino using the Arduino IDE.
3. Ensure the LCD is connected properly to the Arduino.

### Raspberry Pi Setup
1. Install the required Python libraries listed in `requirements.txt` using pip.
2. Connect the Raspberry Pi to the Arduino via USB.
3. Run the `main.py` script to start the voice recognition and cooking step navigation.

## Usage
- Use voice commands such as "étape suivante" (next step) and "étape précédente" (previous step) to navigate through the cooking steps.
- The current step will be displayed on the Arduino's LCD and read aloud using the `espeak` command on the Raspberry Pi.

## Contributing
Contributions are welcome! Please feel free to submit issues or pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.