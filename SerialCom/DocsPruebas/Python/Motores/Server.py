import socket
import time
import serial

time.sleep(30)

# Arduino Configuration
arduino_mov_port = '/dev/ttyACM1'  # Adjust the port based on your setup
arduino_baud_rate = 9600
arduino_mov_serial = serial.Serial(arduino_mov_port, arduino_baud_rate, timeout=1)

# UDP Server Configuration
server_ip = '192.168.0.100'
server_port = 2222                                                                            
buffer_size = 1024

def send_command_to_arduino_mov(velocidad, angulo):
    """
    Manda un comando al Arduino para controlar los motores

    Args:
        velocidad (int): Velocidad del motor (0 - 255)
        angulo (int): Angulo del servo (0 - 750)

    Returns:
        None
    """

    command = f"<{velocidad},{angulo};>"
    arduino_mov_serial.write(command.encode('utf-8'))
    time.sleep(1)  # Espera para asegurar que el Arduino procese el comando
    response = arduino_mov_serial.readline().decode('utf-8', errors='replace').strip()
    print("Respuesta del Arduino:", response)

RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPIsocket.bind((server_ip, server_port))
print('Server is Up and Listening...')

while True:
    # Receive message from client
    message, address = RPIsocket.recvfrom(buffer_size)
    message = message.decode('utf-8')
    print('Received Message:', message)
    print('Client Address:', address[0])
    
    velocidad, angulo= message.split(',')
    # Process the message
    send_command_to_arduino_mov(velocidad, angulo)
    
    
    response_msg="Led's updated successfully"
    RPIsocket.sendto(response_msg.encode('utf-8'),address)