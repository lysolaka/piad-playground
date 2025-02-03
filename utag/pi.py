import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pts_helper import get_pts

import serial


# placeholders
def write_tag(data: str):
    print(f"Writing to tag: {data}")


def read_tag() -> tuple[int, str]:
    id = 747236587
    content = input("Input tag data: ")
    return id, content


SIG_END = b"\x04"
SIG_ACK = b"\x06"
SIG_REA = b"\x0e"
SIG_WRT = b"\x0f"

ser = serial.Serial(get_pts("pi"), 9600, timeout=0)
ser.flush()

print("Working in server mode. Press Control-C to exit.")
try:
    while True:
        rx = ser.read(1)
        if rx == SIG_REA:
            print("Place the tag on the sensor")
            id, content = read_tag()
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
            write_tag(content)
            print("Write successful")
            ser.write(SIG_ACK)
except KeyboardInterrupt:
    print("Leaving...")
