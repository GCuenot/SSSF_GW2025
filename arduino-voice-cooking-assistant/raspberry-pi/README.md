# Raspberry Pi Voice Cooking Assistant

This project allows interaction with an Arduino Nano via USB from a Raspberry Pi 4B, using voice recognition to navigate through cooking steps. The current step is displayed on the Arduino's LCD, and the step is read aloud using "espeak" on the Raspberry Pi.

## Components

- **Arduino**: Manages the LCD display and handles serial communication with the Raspberry Pi.
- **Raspberry Pi**: Runs the voice recognition system and communicates with the Arduino to control the flow of cooking steps.

## Setup Instructions

1. **Arduino Setup**:
   - Upload the `cooking_steps.ino` sketch to the Arduino Nano.
   - Ensure the LiquidCrystal_I2C library is installed in your Arduino IDE.

2. **Raspberry Pi Setup**:
   - Install the required Python libraries listed in `requirements.txt`.
   - Connect the Raspberry Pi to the Arduino via USB.

3. **Running the Application**:
   - Execute `main.py` on the Raspberry Pi to start the voice recognition and cooking step navigation.

## Usage

- Use voice commands "étape suivante" to move to the next cooking step and "étape précédente" to go back to the previous step.
- The current cooking step will be displayed on the Arduino's LCD and read aloud by the Raspberry Pi.

## Dependencies

- Ensure you have Python 3 installed on your Raspberry Pi.
- The project requires specific libraries for voice recognition, serial communication, and audio playback, which are listed in `requirements.txt`.

## License

This project is licensed under the MIT License.