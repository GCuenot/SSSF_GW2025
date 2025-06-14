# Arduino Voice Cooking Assistant

This README provides documentation specific to the Arduino part of the project, including setup instructions and usage details.

## Overview

The Arduino Voice Cooking Assistant project allows users to navigate through cooking steps using voice commands. The Arduino Nano is connected to an LCD display that shows the current cooking step, while the Raspberry Pi handles voice recognition and communicates with the Arduino via USB.

## Requirements

- Arduino Nano
- LCD display (I2C compatible)
- HC-SR04 ultrasonic sensor (optional for presence detection)
- USB cable for connection to Raspberry Pi

## Setup Instructions

1. **Hardware Setup:**
   - Connect the LCD display to the Arduino Nano using I2C. Typically, this involves connecting the SDA and SCL pins of the LCD to the corresponding pins on the Arduino.
   - If using an ultrasonic sensor, connect the trig and echo pins to digital pins 8 and 9 on the Arduino.

2. **Software Installation:**
   - Install the Arduino IDE on your computer.
   - Ensure you have the necessary libraries for the LCD display. You can install the `LiquidCrystal_I2C` library via the Library Manager in the Arduino IDE.

3. **Upload the Sketch:**
   - Open the `cooking_steps.ino` file in the Arduino IDE.
   - Select the correct board (Arduino Nano) and port from the Tools menu.
   - Upload the sketch to the Arduino.

## Usage

- Once the Arduino is powered and the sketch is running, it will display the first cooking step on the LCD.
- The Raspberry Pi will listen for voice commands. When a command is recognized, it will send the appropriate command to the Arduino to navigate to the next or previous cooking step.
- The current cooking step will be displayed on the LCD, and the Raspberry Pi will read the step aloud using the `espeak` command.

## Troubleshooting

- Ensure that the Arduino is properly connected to the Raspberry Pi and that the correct serial port is specified in the Raspberry Pi code.
- If the LCD does not display anything, check the connections and ensure that the correct I2C address is used in the Arduino sketch.

## Contribution

Feel free to contribute to this project by submitting issues or pull requests. Your feedback and improvements are welcome!