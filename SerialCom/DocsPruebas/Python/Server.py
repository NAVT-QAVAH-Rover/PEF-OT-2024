import serial
import socket
import time

# Arduino Configuration
arduino_port = '/dev/ttyACM0'  # Adjust the port based on your setup
arduino_baud_rate = 9600
arduino_serial = serial.Serial(arduino_port, arduino_baud_rate, timeout=1)

# UDP Server Configuration
server_ip = '192.168.0.100'
server_port = 2223                                                                            
buffer_size = 1024

def send_command_to_arduino(command):
    arduino_serial.write(command.encode('utf-8'))
    time.sleep(1)
    response = arduino_serial.readline().decode('utf-8', errors='replace').strip()
    print(response)

def main():
    time.sleep(30)  # Delay to allow other processes to initialize

    # Set up UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((server_ip, server_port))
    print('Server is Up and Listening...')

    try:
        while True:
            # Receive message from client
            message, address = udp_socket.recvfrom(buffer_size)
            message = message.decode('utf-8')
            print('Received Message:', message)
            print('Client Address:', address[0])

            # Process the message
            if message == 'ON':
                send_command_to_arduino('on')
            elif message == 'OFF':
                send_command_to_arduino('off')

            # No need to send a response back for on/off commands

    except KeyboardInterrupt:
        udp_socket.close()
        arduino_serial.close()
        print('Server and Serial port closed. Exiting.')

if __name__ == "__main__":
    main()

