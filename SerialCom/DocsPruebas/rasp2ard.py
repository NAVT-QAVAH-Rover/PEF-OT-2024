import serial
import time

# Configura la conexión serial (ajusta '/dev/ttyUSB0' al puerto correcto)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

while True:
    # Reemplaza 'valor' con el comando o valor específico que deseas enviar
    valor = input("Ingresa el valor para el motor: ")
    ser.write(f"{valor}\n".encode('utf-8'))
    time.sleep(1)
