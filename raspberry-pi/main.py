import serial
import sounddevice as sd
import queue
import vosk
import sys
import json
import subprocess
from time import sleep
from serial_comm import SerialComm
from voice_recognition import VoiceRecognition

# Initialize serial communication
serial_comm = SerialComm('/dev/ttyACM0', 9600)

# Initialize voice recognition
voice_recognition = VoiceRecognition()

def main():
    print("Starting the Cooking Assistant...")
    print("Listening for voice commands...")
    
    while True:
        command = voice_recognition.listen()
        if command:
            print("Command received:", command)
            if "étape suivante" in command:
                serial_comm.send_command("next")
                sleep(1)  # Wait for Arduino to process
                current_step = serial_comm.receive_step()
                print("Current step:", current_step)
                subprocess.run(["espeak", current_step])
            elif "étape précédente" in command:
                serial_comm.send_command("prev")
                sleep(1)  # Wait for Arduino to process
                current_step = serial_comm.receive_step()
                print("Current step:", current_step)
                subprocess.run(["espeak", current_step])

if __name__ == "__main__":
    main()