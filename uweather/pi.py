import time
import serial
from bmp280 import BMP280
from smbus2 import SMBus


def make_csv(temp: list[float], pres: list[float]):
    flines = ["time,temperature,pressure\n"]
    for i, k in enumerate(zip(temp, pres)):
        flines.append(f"{i},{k[0]},{k[1]}\n")
    with open("tx_latest.csv", "w") as file:
        file.writelines(flines)


ser = serial.Serial("/dev/ttyS0", 9600, timeout=0)
ser.flush()
bus = SMBus(1)
sensor = BMP280(i2c_dev=bus)

SIG_END = b"\x04"
SIG_ENQ = b"\x05"
SIG_ACK = b"\x06"

print("Waiting for measurements. Press Control-C to exit.")
try:
    while True:
        rx = ser.read(1)
        if rx == SIG_ENQ:
            print(f"[{time.strftime("%H:%M:%S")}] Performing measurement...")
            ser.write(SIG_ACK)
            temp: list[float] = []
            pres: list[float] = []
            for i in range(11):
                temp.append(sensor.get_temperature())
                pres.append(sensor.get_pressure())
                time.sleep(1)
            make_csv(temp, pres)
            with open("tx_latest.csv", "rb") as file:
                ser.write(file.read())
            ser.write(SIG_END)
            print(f"[{time.strftime("%H:%M:%S")}] Done!")
except KeyboardInterrupt:
    print("Leaving...")
