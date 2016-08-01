import socket
import threading
import shelve

d = shelve.open()
HOST = ''
PORT = 9629       
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
conn, addr = s.accept()
print('Connected by', addr)

'''def sendingMsg():
    while True:
        data = input()
        data = data.encode("utf-8")
        conn.send(data)
    conn.close()'''

def gettingMsg():
    global inform
    
    while True:
        data = conn.recv(1024)
        inform = data.split()
        if not data: 
            break
        elif data == 'USER %s\r\n':
            print('230 User logged in') 
        elif data == 'LIST \r\n':
            print('231 Users: ')
            print('%s', inform[1])
        elif data == 'QUIT \r\n':
            print('221 service closing') 
            conn.close()
            s.close()
        else:
            data = str(data).split("b'", 1)[1].rsplit("'",1)[0]
            print(data)

if __name__ == "__main__":    
    #threading._start_new_thread(sendingMsg,())
    threading._start_new_thread(gettingMsg,())

while True:
    pass