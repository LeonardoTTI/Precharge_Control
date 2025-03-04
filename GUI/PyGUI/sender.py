import pyserial
import time

salt = 0
ser = serial.Serial("COM6", 9600) #seleziono una delle porte create con com0com
time.sleep(2)  # Attendi che la porta si apra

while True:
    ser.write(b"#"+salt)
    time.sleep(1)
