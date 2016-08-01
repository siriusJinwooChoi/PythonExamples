'''
Created on 2014. 5. 31.

@author: Sirius
'''

#client program
import socket
import threading

HOST = "127.0.0.1"
PORT = 8089      
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def sendingMsg():
    while True:
        data = input()
        data = bytes(data, "utf-8")
        s.send(data)
    s.close()
    
def gettingMsg():
    while True:
        data = s.recv(1024)
        data = str(data).split("b'", 1)[1].rsplit("'",1)[0]
        print(data)
    s.close()

threading._start_new_thread(sendingMsg,())
threading._start_new_thread(gettingMsg,())

while True:
    pass
