import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pts_helper import get_pts

import serial


def make_csv(data: bytearray):
    data = data[:-1]  # Strip the SIG_END
    with open("rx_latest.csv", "w") as file:
        file.write(data.decode())


ser = serial.Serial(get_pts("ad"), 9600, timeout=0)
ser.flush()
SIG_END = b"\x04"
SIG_ENQ = b"\x05"
SIG_ACK = b"\x06"

rx_buf = bytearray()

print("Asking Raspberry Pi for measurements...")
ser.write(SIG_ENQ)
while True:
    rx = ser.read(1)
    if rx == SIG_ACK:
        break
print("Measuring...   ", end="")

# make it look cool (gentoo spinner)
seq = "/-\\|/-\\|/-\\|/-\\|\\-/|\\-/|\\-/|\\-/|"
i = 0
while True:
    rx = ser.read(1)
    if rx:
        rx_buf += rx
        if rx_buf[-1:] == bytearray(SIG_END):
            make_csv(rx_buf)
            break
    else:
        sys.stdout.write("\b\b " + seq[i])
        sys.stdout.flush()
        i = (i + 1) % len(seq)

print("\nMeasurement complete.")
# TODO: do matplotlib graph
