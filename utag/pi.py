import serial
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


SIG_END = b"\x04"
SIG_ACK = b"\x06"
SIG_REA = b"\x0e"
SIG_WRT = b"\x0f"

ser = serial.Serial("/dev/ttyS0", 9600, timeout=0)
ser.flush()
reader = SimpleMFRC522()

print("Working in server mode. Press Control-C to exit.")
try:
    while True:
        rx = ser.read(1)
        if rx == SIG_REA:
            print("Place the tag on the sensor")
            id, content = reader.read()
            ser.write(f"{id};{content}".encode())
            ser.write(SIG_END)
            while True:
                rx = ser.read(1)
                if rx == SIG_ACK:
                    break
            print("Read successful")

        elif rx == SIG_WRT:
            rx_buf = bytearray()
            while True:
                rx_buf += ser.read(1)
                if rx_buf[-1:] == bytearray(SIG_END):
                    break
            content = rx_buf[:-1].decode()
            print("Place the tag on the sensor")
            reader.write(content)
            print("Write successful")
            ser.write(SIG_ACK)
except KeyboardInterrupt:
    print("Leaving...")
finally:
    GPIO.cleanup()
