import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import serial
import serial.tools.list_ports
import threading
import csv
import time
from tkinter import scrolledtext, StringVar

isListening = False

class TelemetryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CAN Telemetry App")
        self.root.minsize(800, 600)  # Set minimum size for the window

        self.serial_connection = None
        self.stop_thread = False

        # Serial Port and Baud Rate Selection
        self.com_var = StringVar()
        self.baud_var = StringVar(value='9600')

        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.com_label = ttk.Label(self.frame, text="COM Port:")
        self.com_label.grid(row=0, column=0, padx=5)
        self.com_select = ttk.Combobox(self.frame, textvariable=self.com_var, values=self.get_com_ports(), width=10)
        self.com_select.grid(row=0, column=1, padx=5)

        self.baud_label = ttk.Label(self.frame, text="Baud Rate:")
        self.baud_label.grid(row=0, column=2, padx=5)
        self.baud_select = ttk.Combobox(self.frame, textvariable=self.baud_var, values=['4800', '9600', '19200', '38400', '57600', '112500', '230400', '460800', '921600'], width=10)
        self.baud_select.grid(row=0, column=3, padx=5)

        self.start_button = ttk.Button(self.frame, text="Start Listening", command=self.start_listening, bootstyle=SUCCESS)
        self.start_button.grid(row=0, column=4, padx=5)
        self.stop_button = ttk.Button(self.frame, text="Stop Listening", command=self.stop_listening, bootstyle=DANGER, state=DISABLED)
        self.stop_button.grid(row=0, column=5, padx=5)

        # Log Box
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10, fill='both', expand=True)  # Expand frame with window resize

        self.log_box = scrolledtext.ScrolledText(self.main_frame, height=20, width=80, state='disabled')
        self.log_box.grid(row=0, column=0, padx=10, sticky='nsew')  # Sticky to stretch with resize

        # Signal values beside the log box
        self.signal_frame = ttk.Frame(self.main_frame)
        self.signal_frame.grid(row=0, column=1, padx=10, sticky='n')  # Sticky north to keep signals at the top

        self.signal1_var = StringVar(value="Signal 1: 0")
        self.signal2_var = StringVar(value="Signal 2: 0")
        self.signal3_var = StringVar(value="Signal 3: 0")
        self.signal4_var = StringVar(value="Signal 4: 0")

        self.signal1_label = ttk.Label(self.signal_frame, textvariable=self.signal1_var)
        self.signal1_label.pack(pady=5)

        self.signal2_label = ttk.Label(self.signal_frame, textvariable=self.signal2_var)
        self.signal2_label.pack(pady=5)

        self.signal3_label = ttk.Label(self.signal_frame, textvariable=self.signal3_var)
        self.signal3_label.pack(pady=5)

        self.signal4_label = ttk.Label(self.signal_frame, textvariable=self.signal4_var)
        self.signal4_label.pack(pady=5)

        # Input Box to send CAN frames
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(padx=10, pady=10, fill='x', expand=True)  # Expand frame with window resize

        self.input_var = StringVar()
        self.input_entry = ttk.Entry(self.input_frame, textvariable=self.input_var, width=50)
        self.input_entry.grid(row=0, column=0, padx=5, sticky='ew')  # Sticky east-west to stretch horizontally
        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.send_message, bootstyle=INFO)
        self.send_button.grid(row=0, column=1, padx=5)

        # Make log_box and input_entry resizable
        self.main_frame.grid_columnconfigure(0, weight=1)  # Allow column 0 (log box) to expand
        self.main_frame.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
        self.input_frame.grid_columnconfigure(0, weight=1)  # Allow input entry to expand

        # Log file setup
        self.log_file = open(f"can_telemetry_log_{time.strftime('%Y%m%d-%H%M%S')}.csv", mode='w', newline='')
        self.csv_writer = csv.writer(self.log_file)
        self.csv_writer.writerow(["Timestamp", "Direction", "Message"])

    def get_com_ports(self):
        """Get available COM ports."""
        return [port.device for port in serial.tools.list_ports.comports()]

    def start_listening(self):
        """Start listening to CAN frames."""
        try:
            self.serial_connection = serial.Serial(self.com_var.get(), self.baud_var.get(), timeout=1)
            self.stop_thread = False
            self.listener_thread = threading.Thread(target=self.listen_to_port)
            self.listener_thread.start()
            self.start_button.config(state=DISABLED)
            self.stop_button.config(state=NORMAL)
            isListening = True
        except Exception as e:
            self.update_log(f"Error: {e}")

    def stop_listening(self):
        """Stop listening to CAN frames."""
        self.stop_thread = True
        self.listener_thread.join()
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)

    def listen_to_port(self):
        """Listen to the serial port for incoming CAN frames."""
        while not self.stop_thread:
            if self.serial_connection.in_waiting > 0:
                message = self.serial_connection.readline().decode('utf-8').strip()
                self.update_log(f"Received: {message}")
                self.csv_writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), "RX", message])

                # Simulate signal value extraction from the message
                # Assume the message format is like: "S1:12,S2:45,S3:78,S4:90"
                values = self.parse_signals(message)
                self.update_signals(values)

    def parse_signals(self, message):
        """Parse signal values from the CAN message."""
        values = {'S1': 0, 'S2': 0, 'S3': 0, 'S4': 0}
        try:
            for pair in message.split(','):
                signal, value = pair.split(':')
                values[signal.strip()] = int(value.strip())
        except:
            pass
        return values

    def update_signals(self, values):
        """Update the signal labels with new values."""
        self.signal1_var.set(f"Signal 1: {values['S1']}")
        self.signal2_var.set(f"Signal 2: {values['S2']}")
        self.signal3_var.set(f"Signal 3: {values['S3']}")
        self.signal4_var.set(f"Signal 4: {values['S4']}")

    def send_message(self):
        """Send a CAN frame."""
        message = self.input_var.get().strip()
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write((message + '\n').encode('utf-8'))
            self.update_log(f"Sent: {message}")
            self.csv_writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), "TX", message])
        self.input_var.set('')

    def update_log(self, message):
        """Update the log box with a new message."""
        self.log_box.config(state='normal')
        self.log_box.insert('end', message + '\n')
        self.log_box.config(state='disabled')
        self.log_box.yview('end')

    def on_close(self):
        """Handle app closing."""
        if isListening:
            self.stop_listening()
        self.log_file.close()
        self.root.destroy()

# Create and run the app
root = ttk.Window(themename="superhero")
app = TelemetryApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_close)
root.mainloop()
