# CODE FOR COMPUTER CLIENT

import socket

serverAddress=('192.168.0.100',2223)
bufferSize=1024
UDPClient=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    cmd=input('Dame el ID del Servomotor y el valor para el ángulo del servo (ID1, Val1, ID2, Val2, ...): ')
    cmd= cmd.encode('utf-8')
    UDPClient.sendto(cmd,serverAddress)
    data,address=UDPClient.recvfrom(bufferSize)
    data=data.decode('utf-8')
    print('Data from Server',data)
    print('Server IP Address: ',address[0])
    print('Server Port: ',address[1])
