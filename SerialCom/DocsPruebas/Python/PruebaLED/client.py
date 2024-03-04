import socket

serverAddress = ('192.168.0.100', 2222)
bufferSize = 1024
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Ingresar el estado para ambos LEDs en la misma línea, separados por una coma
    leds_state = input('Enter MOTOR 1 and MOTOR 2 (ON or OFF for each, separated by a comma): ')
    
    # Separar los estados de los LEDs
    cmd_led1, cmd_led2 = leds_state.split(',')
    
    # Formar el mensaje con ambos estados
    message = f"{cmd_led1},{cmd_led2}"
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


