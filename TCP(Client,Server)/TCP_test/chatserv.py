from socket import *
import socket, sys, threading, time, re, sqlite3

con_temp = sqlite3.connect('Users.db')
cur = con_temp.cursor()
cur.execute('CREATE TABLE Users(ID TEXT, PASSWORD TEXT)')
con_temp.close()

CRLF = re.compile(r'(.*?)\r\n')
lists = []
clients = dict()
message = {
           230: '230 User logged in',
           231: '231 Users:',
           221: '221 service closing',
           299: '299',
           200: '200 OK', 
           500: '500 Syntax error',
           530: '530 Not logged in',
           531: '531 Invalid user or password'
           }

class ChatServer(threading.Thread):
    global clients
    def __init__(self, client):
        threading.Thread.__init__(self)

        self.client_sock, self.client_addr = client
        clients[self.client_sock.fileno()] = self.client_sock
        self.client_sock_temp = self.client_sock
        self.UserID = ''
        self.debug = True
    
    def removeClient(self, sock):
        del clients[sock.fileno()]
        sock.close()
        self.cli_sock = ''
    
    def sendResponse(self, connection, code, arg=None):
        response = message[code]
        if arg:
            response += ' ' + arg 
        response += '\r\n'
        connection.send(bytes(response, encoding='UTF-8'))
        if self.debug:
            print('<', response)
            
    def Requestmsg(self, connection, request):
        global cur, lists
        con = sqlite3.connect('Users.db')
        cur = con.cursor()
        user = request.split()
        if self.debug:
            print('>', request)
        words = request.split(None, 1)
        command = words[0]
        
        if command == 'USER':
            if(len(user) == 2):
                self.sendResponse(connection, 531)
            else:
                cur.execute('SELECT * FROM Users WHERE ID = "%s"' % user[1])
                if cur.fetchone() :
                    cur.execute('SELECT * FROM Users WHERE ID = "%s"' % user[1])
                    if cur.fetchone()[1] == user[2] :
                        self.sendResponse(connection, 230)
                    else:
                        self.sendResponse(connection, 531)
                else :
                    self.sendResponse(connection, 230)
                    cur.execute('INSERT INTO Users VALUES(?, ?)', (user[1], user[2]))
                    con.commit()
                    
        elif command == 'LIST':
            cur.execute('SELECT ID FROM Users')
            for userid in cur.fetchall():
                lists += userid
            lists = ' '.join(lists)      
            self.sendResponse(connection, 231, lists)
            lists = []
        
        elif command == 'QUIT':
            self.sendResponse(connection, 221)
            self.removeClient(connection)
            connection.close()
        
        elif command == 'FROM':
            for self.cli_sock_tmp in clients.values():
                if self.cli_sock_tmp is not connection:
                    client = self.cli_sock_tmp
                    self.sendResponse(client, 299, request)
            self.sendResponse(connection, 200)
        else:
            self.sendResponse(connection, 500)
    
    def run(self):
        while True:
            if self.debug:
                print('Wait for readable sockets:', [sock.fileno() for sock in clients.values()])
            if self.client_sock is not '':
                data = self.client_sock.recv(1024).decode()
            else:
                break
            time.sleep(1) 
            if not data: 
                sock.close()
            else:
                for line in CRLF.findall(data):
                    self.Requestmsg(self.client_sock, line)

if __name__ == "__main__":    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.bind(('127.0.0.1', 9629)) 
    sock.listen(10)
    #clients[sock.fileno()] = sock
    print('Wait for readable sockets:', [sockobj.fileno() for sockobj in clients.values()])
    while True: 
        server = sock.accept()
        ChatServer(server).start()