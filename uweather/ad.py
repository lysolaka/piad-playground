import sys
from pydwf import DwfLibrary, PyDwfError
from pydwf.utilities import openDwfDevice


def make_csv(data: bytearray):
    data = data[:-1]  # Strip the SIG_END
    with open("rx_latest.csv", "w") as file:
        file.write(data.decode())


SIG_END = b"\x04"
SIG_ENQ = b"\x05"
SIG_ACK = b"\x06"

UART_TX = 8
UART_RX = 0

try:
    dwf = DwfLibrary()
    device = openDwfDevice(dwf)
    uart = device.protocol.uart

    uart.reset()
    uart.rateSet(9600.0)
    uart.bitsSet(8)
    uart.paritySet(0)
    uart.stopSet(1)
    uart.txSet(UART_TX)
    uart.rxSet(UART_RX)
    uart.rx(0)

    rx_buf = bytearray()

    print("Asking Raspberry Pi for measurements...")
    uart.tx(SIG_ENQ)
    while True:
        rx, _ = uart.rx(1)
        if rx == SIG_ACK:
            break
    print("Measuring...   ", end="")

    # make it look cool (gentoo spinner)
    seq = "/-\\|/-\\|/-\\|/-\\|\\-/|\\-/|\\-/|\\-/|"
    i = 0
    while True:
        rx, _ = uart.rx(1)
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
    device.close()

except PyDwfError as exception:
    print("PyDwfError:", exception)
except KeyboardInterrupt:
    print("Keyboard interrupt, ending.")
# TODO: do matplotlib graph
