# Arduino Cooking Steps Documentation

This README file provides instructions for the Arduino part of the Cooking Assistant project. It includes details on how to upload the Arduino sketch and connect the necessary hardware.

## Overview

The `cooking_steps.ino` file contains the Arduino sketch that manages the cooking steps. It initializes an LCD display, defines a series of cooking steps, and handles serial commands from the Raspberry Pi to navigate through these steps.

## Requirements

- Arduino Uno R3 or compatible board
- LCD display (I2C compatible)
- Jumper wires for connections
- USB cable to connect the Arduino to the Raspberry Pi

## Uploading the Sketch

1. Open the Arduino IDE on your computer.
2. Connect your Arduino Uno to your computer using the USB cable.
3. Open the `cooking_steps.ino` file in the Arduino IDE.
4. Select the correct board and port from the Tools menu.
5. Click on the upload button (right arrow icon) to upload the sketch to the Arduino.

## Wiring the LCD Display

Connect the LCD display to the Arduino as follows (assuming a common I2C interface):

- VCC to 5V
- GND to GND
- SDA to A4 (or the SDA pin on your board)
- SCL to A5 (or the SCL pin on your board)

## Running the Project

Once the sketch is uploaded and the hardware is connected:

1. Connect the Arduino to the Raspberry Pi via USB.
2. Ensure that the Raspberry Pi is set up with the necessary Python scripts to communicate with the Arduino.
3. Run the Raspberry Pi application to start listening for voice commands.

## Troubleshooting

- If the LCD does not display anything, check the wiring and ensure the correct I2C address is used in the sketch.
- Make sure the Arduino is properly connected to the Raspberry Pi and that the correct serial port is specified in the Raspberry Pi scripts.

## Conclusion

This Arduino sketch is a crucial part of the Cooking Assistant project, allowing for interactive cooking steps displayed on an LCD and controlled via voice commands from the Raspberry Pi.