import serial
import tkinter as tk
from tkinter import messagebox
from pydwf import DwfLibrary, PyDwfError
from pydwf.utilities import openDwfDevice
from pydwf.core.api.protocol_uart import ProtocolUART


SIG_END = b"\x04"
SIG_ACK = b"\x06"
SIG_REA = b"\x0e"
SIG_WRT = b"\x0f"
UART_TX = 8
UART_RX = 0


class Window:
    def __init__(self, root: tk.Tk, uart: ProtocolUART):
        self.root = root
        self.root.title("UART Tag")

        self.id_lb = tk.Label(root, text="Tag ID:")
        self.id_lb.grid(row=0, column=0, padx=10, pady=5)

        self.id_box = tk.Entry(root, state="readonly")
        self.id_box.grid(row=0, column=1, padx=10, pady=5)

        self.text_lb = tk.Label(root, text="Tag data:")
        self.text_lb.grid(row=1, column=0, padx=10, pady=5)

        self.text_box = tk.Entry(root)
        self.text_box.grid(row=1, column=1, padx=10, pady=5)

        self.write_bt = tk.Button(root, text="Send", command=self.write_tag)
        self.write_bt.grid(row=2, column=0, padx=10, pady=5)

        self.read_bt = tk.Button(root, text="Read", command=self.read_tag)
        self.read_bt.grid(row=2, column=1, padx=10, pady=5)

        uart.reset()
        uart.rateSet(9600.0)
        uart.bitsSet(8)
        uart.paritySet(0)
        uart.stopSet(1)
        uart.txSet(UART_TX)
        uart.rxSet(UART_RX)
        uart.rx(0)
        self.uart = uart

    def update_id_box(self, text: str):
        self.id_box.config(state="normal")
        self.id_box.delete(0, tk.END)
        self.id_box.insert(0, text)
        self.id_box.config(state="readonly")

    def write_tag(self):
        self.update_id_box("ID is constant")
        content = self.text_box.get()
        messagebox.showinfo(title="Info", message="Place the tag on the sensor")
        self.uart.tx(SIG_WRT)
        self.uart.tx(content.encode())
        self.uart.tx(SIG_END)
        while True:
            rx, _ = self.uart.rx(1)
            if rx == SIG_ACK:
                messagebox.showinfo(title="Info", message="Tag successfully written")
                break

    def read_tag(self):
        rx_buf = bytearray()
        messagebox.showinfo(title="Info", message="Place the tag on the sensor")
        self.uart.tx(SIG_REA)
        while True:
            rx, _ = self.uart.rx(1)
            if rx:
                rx_buf += rx
                if rx_buf[-1:] == bytearray(SIG_END):
                    break
        self.uart.tx(SIG_ACK)
        rx_buf = rx_buf[:-1].decode()
        id, content = rx_buf.split(";", 1)
        messagebox.showinfo(title="Info", message="Tag successfully read")
        self.update_id_box(id)
        self.text_box.delete(0, tk.END)
        self.text_box.insert(0, content)

if __name__ == "__main__":
    try:
        dwf = DwfLibrary()
        with openDwfDevice(dwf) as device:
            root = tk.Tk()
            app = Window(root, device.protocol.uart)
            root.mainloop()
    except PyDwfError as exception:
        print("PyDwfError:", exception)
    except KeyboardInterrupt:
        print("Keyboard interrupt, ending.")
