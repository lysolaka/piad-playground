import tkinter as tk
import threading
import queue
from pydwf import DwfLibrary, PyDwfError
from pydwf.utilities import openDwfDevice
from pydwf.core.api.protocol_uart import ProtocolUART

SIG_END = b"\x03"
UART_TX = 8
UART_RX = 0


class Window:
    def __init__(self, root: tk.Tk, uart: ProtocolUART):
        self.root = root
        self.root.title("UART Pager")

        self.msg_q: queue.Queue[str] = queue.Queue()

        self.rx_lb = tk.Label(root, text="Last recieved:")
        self.rx_lb.grid(row=0, column=0, padx=10, pady=5)

        self.rx_txt = tk.Entry(root, state="readonly")
        self.rx_txt.grid(row=0, column=1, padx=10, pady=5)

        self.tx_lb = tk.Label(root, text="Send text:")
        self.tx_lb.grid(row=1, column=0, padx=10, pady=5)

        self.tx_txt = tk.Entry(root)
        self.tx_txt.grid(row=1, column=1, padx=10, pady=5)

        self.send_bt = tk.Button(root, text="Send", command=self.msg_tx)
        self.send_bt.grid(row=2, column=0, columnspan=2, pady=10)

        uart.reset()
        uart.rateSet(9600.0)
        uart.bitsSet(8)
        uart.paritySet(0)
        uart.stopSet(1)
        uart.txSet(UART_TX)
        uart.rxSet(UART_RX)
        uart.rx(0)

        self.uart = uart
        thread = threading.Thread(target=self.rx_thread, daemon=True)
        thread.start()

        self.check_msg_q()

    def set_rx_txt(self, content: str):
        self.rx_txt.config(state="normal")
        self.rx_txt.delete(0, tk.END)
        self.rx_txt.insert(0, content)
        self.rx_txt.config(state="readonly")

    def rx_thread(self):
        rx_buf = bytearray()
        while True:
            rx, _ = self.uart.rx(1)
            if rx:
                rx_buf += rx
                if rx_buf[-1:] == bytearray(SIG_END):
                    msg = rx_buf[:-1].decode()
                    self.msg_q.put(msg)
                    rx_buf.clear()

    def check_msg_q(self):
        try:
            while not self.msg_q.empty():
                rx = self.msg_q.get_nowait()
                self.set_rx_txt(rx)
        except queue.Empty:
            pass

        self.root.after(250, self.check_msg_q)

    def msg_tx(self):
        tx = self.tx_txt.get()
        self.uart.tx(tx.encode())
        self.uart.tx(SIG_END)


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

