'''
Created on 2014. 6. 5.

@author: Sirius
'''
import socket

class chatServer():
    def __init__(self, client):
        
        self.client_sock, self.client_addr = client
        '''
        threading.Thread.__init__(self)
        '''
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", 9629))
        server_socket.listen(5)
        print("TCP Server Waiting for client on port 9629")

        while 1:
            client_socket, address = server_socket.accept()
            print("I got a connection from", address)
            while 1:
                data = input("Input your message to Other : ")
                if(data == 'Q' or data == 'q' or data == 'QUIT' or data == 'quit'):
                    client_socket.send(data.encode())
                    client_socket.close()
                    break;
                else:
                    client_socket.send(data.encode())
            
                data = client_socket.recv(512).decode()
                if(data == 'q' or data == 'Q' or data == 'QUIT' or data == 'quit'):
                    client_socket.close()
                    break;
                else:
                    print("Received message : ", data)
            break;
        server_socket.close()
        print("Socket closed... END")             

if __name__ == "__main__":
    chatServer()
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 9629))
    sock.listen(10)
    
    while True:
        pass
    
    server = sock.accept()
    chatServer(server).start()
    '''