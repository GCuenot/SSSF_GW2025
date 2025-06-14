import serial
import time

class SerialComm:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None

    def connect(self):
        self.serial = serial.Serial(self.port, self.baudrate)
        time.sleep(2)  # Wait for the connection to establish

    def send_command(self, command):
        if self.serial and self.serial.is_open:
            self.serial.write((command + '\n').encode())

    def read_response(self):
        if self.serial and self.serial.is_open:
            if self.serial.in_waiting > 0:
                return self.serial.readline().decode().strip()
        return None

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()