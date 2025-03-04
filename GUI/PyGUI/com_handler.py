import serial
import csv
import threading
import queue
import time

class SerialHandler:
    def __init__(self, data_queue):
        self.serial_port = None
        self.running = False
        self.data_queue = data_queue
        self.log_file = None
        self.csv_writer = None
        self.logging_active = False

    def start_reading(self, port, baudrate=9600):
        self.serial_port = serial.Serial(port, baudrate, timeout=1)
        self.running = True
        self.thread = threading.Thread(target=self.read_data)
        self.thread.start()

    def stop_reading(self):
        self.running = False
        self.stop_logging()  # Chiude il file di log prima di terminare
        if self.serial_port:
            self.serial_port.close()

    def read_data(self):
        while self.running and self.serial_port:
            try:
                line = self.serial_port.readline().decode().strip()
                if line:
                    value = float(line)
                    timestamp = time.time()
                    self.data_queue.put((timestamp, value))
                    if self.logging_active and self.csv_writer:
                        self.csv_writer.writerow([timestamp, value])
            except Exception as e:
                print("Errore nella lettura:", e)

    def start_logging(self):
        self.log_file = open("log.csv", "w", newline="")
        self.csv_writer = csv.writer(self.log_file)
        self.csv_writer.writerow(["Timestamp", "Value"])
        self.logging_active = True

    def stop_logging(self):
        if self.log_file:
            self.log_file.close()
        self.logging_active = False
