'''
Created on 2014. 8. 11.

@author: Sirius
'''
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9629))
while 1:
    data = client_socket.recv(512).decode()
    if(data == 'q' or data == 'Q' or data == 'QUIT' or data == 'quit'):
        client_socket.close()
        break;
    else:
        print("Received message : ", data)
        data = input("Input your message to Other:")
        if(data == 'q' or data == 'Q' or data == 'QUIT' or data == 'quit'):
            client_socket.send(data.encode())
            client_socket.close()
            break;
        else:
            client_socket.send(data.encode())
print("Socket closed...END.")