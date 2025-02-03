import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pts_helper import get_pts

import serial
import tkinter as tk
from tkinter import messagebox

SIG_END = b"\x04"
SIG_ACK = b"\x06"
SIG_REA = b"\x0e"
SIG_WRT = b"\x0f"


class Window:
    def __init__(self, root: tk.Tk):
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

        self.ser = serial.Serial(get_pts("ad"), 9600, timeout=0)
        self.ser.flush()

    def update_id_box(self, text: str):
        self.id_box.config(state="normal")
        self.id_box.delete(0, tk.END)
        self.id_box.insert(0, text)
        self.id_box.config(state="readonly")

    def write_tag(self):
        self.update_id_box("ID is constant")
        content = self.text_box.get()
        messagebox.showinfo(title="Info", message="Place the tag on the sensor")
        self.ser.write(SIG_WRT)
        self.ser.write(content.encode())
        self.ser.write(SIG_END)
        while True:
            rx = self.ser.read(1)
            if rx == SIG_ACK:
                messagebox.showinfo(title="Info", message="Tag successfully written")
                break

    def read_tag(self):
        rx_buf = bytearray()
        messagebox.showinfo(title="Info", message="Place the tag on the sensor")
        self.ser.write(SIG_REA)
        while True:
            rx = self.ser.read(1)
            if rx:
                rx_buf += rx
                if rx_buf[-1:] == bytearray(SIG_END):
                    break
        self.ser.write(SIG_ACK)
        rx_buf = rx_buf[:-1].decode()
        id, content = rx_buf.split(";", 1)
        messagebox.showinfo(title="Info", message="Tag successfully read")
        self.update_id_box(id)
        self.text_box.delete(0, tk.END)
        self.text_box.insert(0, content)

if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
