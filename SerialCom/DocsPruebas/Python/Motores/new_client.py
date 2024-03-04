import socket

serverAddress = ('192.168.0.100', 2222)
bufferSize = 1024
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Ingresar el estado para motores y servos en la misma línea, separados por una coma
    input_state = input('Enter velocity and angle (Velocity 0 - 255 [Recomended more than 100] , Angle 0 - 750 [Center 375]): ')
    
    # Separar los estados de los LEDs
    velocidad, angulo = input_state.split(',')
    
    # Formar el mensaje con ambos estados
    message = f"{velocidad},{angulo}"
    message = message.encode('utf-8')
    
    # Enviar el mensaje al servidor
    UDPClient.sendto(message, serverAddress)
    
    # Recibir y decodificar la respuesta del servidor
    data, address = UDPClient.recvfrom(bufferSize)
    data = data.decode('utf-8')
    
    # Imprimir la respuesta del servidor junto con la dirección IP y el puerto
    print('Data from Server:', data)
    print('Server IP Address:', address[0])
    print('Server Port:', address[1])