# CODE FOR RASPBERRY PI SERVER

import serial
import socket
import time
import threading

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

def handle_motor_movement(device_id, motor_value):
    command = f"{device_id},{motor_value}"  # Format the command
    print(f"Sending to Arduino in a separate thread: {command}")
    send_command_to_arduino(command)

def main():
    time.sleep(50)  # Delay to allow other processes to initialize

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
            values = message.split(',')  # Split the message by comma
            for i in range(0, len(values), 2):
                device_id = values[i]
                motor_value = values[i+1]
                
                # Create a new thread for each motor movement command
                movement_thread = threading.Thread(target=handle_motor_movement, args=(device_id, motor_value))
                movement_thread.start()
            
            # No need to send a response back for on/off commands

    except KeyboardInterrupt:
        udp_socket.close()
        arduino_serial.close()
        print('Server and Serial port closed. Exiting.')

if __name__ == "__main__":
    main()