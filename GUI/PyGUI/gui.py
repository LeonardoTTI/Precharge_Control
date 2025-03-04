import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial.tools.list_ports
from com_handler import SerialHandler
import threading
import queue
import time
from sys import exit

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Data Logger")
        
        # Coda per la gestione dei dati
        self.data_queue = queue.Queue()

        # Istanza del gestore seriale
        self.serial_handler = SerialHandler(self.data_queue)

        # Frame superiore
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Menu a tendina per le COM
        self.com_var = tk.StringVar()
        self.com_dropdown = ttk.Combobox(top_frame, textvariable=self.com_var, state="readonly")
        self.com_dropdown.pack(side=tk.LEFT, padx=5)
        self.refresh_com_ports()

        # Pulsanti di connessione
        self.start_button = tk.Button(top_frame, text="Start", bg="green", fg="white", command=self.start_connection)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(top_frame, text="Stop", bg="red", fg="white", command=self.stop_connection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Frame inferiore per grafico e pulsanti
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Grafico Matplotlib
        self.fig, self.ax = plt.subplots()
        self.x_data = []
        self.y_data = []
        self.line, = self.ax.plot([], [], 'b-')

        self.ax.set_title("Dati in tempo reale")
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Valore")
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(-10, 10)  # Modificare in base ai dati previsti

        self.canvas = None
        self.create_matplotlib_canvas(bottom_frame)

        # Pulsanti per gestione log
        self.log_button = tk.Button(bottom_frame, text="Start Log", bg="blue", fg="white", command=self.start_logging)
        self.log_button.pack(side=tk.LEFT, padx=5)

        self.stop_log_button = tk.Button(bottom_frame, text="Stop Log", bg="yellow", fg="black", command=self.stop_logging, state=tk.DISABLED)
        self.stop_log_button.pack(side=tk.LEFT, padx=5)

        # Avvio aggiornamento grafico
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=1000)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def create_matplotlib_canvas(self, parent):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def refresh_com_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.com_dropdown["values"] = ports
        if ports:
            self.com_var.set(ports[0])

    def start_connection(self):
        port = self.com_var.get()
        if port:
            self.serial_handler.start_reading(port)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_connection(self):
        self.serial_handler.stop_reading()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def start_logging(self):
        if not self.serial_handler.running:
            print("Errore: avvia prima la connessione seriale.")
            return  
        self.serial_handler.start_logging()
        self.log_button.config(state=tk.DISABLED)
        self.stop_log_button.config(state=tk.NORMAL)

    def stop_logging(self):
        self.serial_handler.stop_logging()
        self.log_button.config(state=tk.NORMAL)
        self.stop_log_button.config(state=tk.DISABLED)

    def on_closing(self):
        self.serial_handler.stop_reading()  # Interrompe la lettura e chiude il file di log
        self.root.destroy()  # Chiude la finestra
        exit(0)

    def update_plot(self, frame):
        while not self.data_queue.empty():
            timestamp, value = self.data_queue.get()
            self.x_data.append(time.time() % 30)
            self.y_data.append(value)

        if len(self.x_data) > 30:
            self.x_data = self.x_data[-30:]
            self.y_data = self.y_data[-30:]

        self.line.set_data(self.x_data, self.y_data)
        if self.x_data:  
            self.ax.set_xlim(max(0, self.x_data[0]), max(30, self.x_data[-1]))  
        else:  
            self.ax.set_xlim(0, 30)  # Limiti di default quando non ci sono dati
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialGUI(root)
    root.mainloop()
