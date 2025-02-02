import sys
import serial
import time
import threading

SIG_END = b"\x03"

ser = serial.Serial("/dev/ttyS0", 9600, timeout=0)


def update_rx():
    rx_buf = bytearray()
    while True:
        rx = ser.read(1)
        if rx:
            rx_buf += rx
            if rx_buf[-1:] == bytearray(SIG_END):
                msg = rx_buf[:-1].decode()
                rx_buf.clear()
                sys.stdout.write("\x1b[s")
                sys.stdout.write("\x1b[1F\x1b[2K")
                sys.stdout.write(f"Last recieved: {msg}\n")
                sys.stdout.write("\x1b[u")
                sys.stdout.flush()
                time.sleep(0.25)


thread = threading.Thread(target=update_rx, daemon=True)
thread.start()

while True:
    print()
    tx = input("Send text: ")
    ser.write(tx.encode())
    ser.write(SIG_END)
