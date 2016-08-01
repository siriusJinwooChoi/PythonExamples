# client program
from socket import socket, AF_INET, SOCK_STREAM
import sys, time, threading
import tkinter as tk
from tkinter import *
'''
from tkinter.colorchooser import askcolor
from tkinter.messagebox import *
'''

class ChatClient():
    def __init__(self, host, port):
        global Users
        self.user, self.debug = None, False
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.host, self.port = host, port
        self.sock.connect((self.host, self.port))
        
        self.index = Tk()
        self.index.title('index')
        self.index.geometry("200x50")
        form = Frame(self.index).pack()        
        Button(self.index, text="Login", command=self.loginview, fg="darkgreen").pack(fill=X)
        Button(self.index, text="Quit", command=self.index.quit, fg="red").pack(fill=X)
    
    def loginview(self):
        global Users
        Users = {}
        self.loginview = Tk()
        self.loginview.title('login window')
        form = Frame(self.loginview)
        form.pack()
        
        for (ix, label) in enumerate(('name', 'password')):
            lab = Label(form, text=label)
            ent = Entry(form)
            imsi3 = imsi3(form, text=label)
            lab.grid(row=ix, column=0)
            ent.grid(row=ix, column=1)
            imsi3.grid(row=ix, column=2)
            Users[label] = ent
        Button(self.loginview, text="로그인", command=self.commandWindow).pack(fill=X)
        Button(self.loginview, text="Quit", command=self.loginview.quit).pack(fill=X)
    
    def commandWindow(self):
        global Entermsg, mylist
        
        self.login()
        self.mainconsole = Tk()
        self.mainconsole.title('Main Console')
        form = Frame(self.mainconsole)
        form.pack()
        form2 = Frame(self.mainconsole)
        form2.pack()
        scrollbar = Scrollbar(form)
        scrollbar.pack(side=RIGHT, fill=Y)
        mylist = Listbox(form, yscrollcommand=scrollbar.set)
        mylist.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=mylist.yview)
        Lb1 = Label(form2, text="Message")
        Lb1.pack(side=LEFT)
        Entermsg = Entry(form2, bd=3)
        Entermsg.pack(side=RIGHT)
        Button(self.mainconsole, text="Send", command=self.Sendview).pack(side=LEFT)
        Button(self.mainconsole, text="List", command=self.Listview).pack(side=LEFT)
        Button(self.mainconsole, text="Debug", command=self.Debugview).pack(side=LEFT)
        Button(self.mainconsole, text="Quit", command=self.Quitgoing).pack(side=RIGHT)
    
    def Debugview(self):
        global debug
        self.debug = False if self.debug else True
        if self.debug is True:
            mylist.insert(END, 'debug = True')
        else:
            mylist.insert(END, 'debug = False')
    
    def Listview(self):
        request = 'LIST\r\n'
        if self.debug is True:
            mylist.insert(END, '> LIST')
        self.sock.send(request.encode('UTF-8'))
        
    def Sendview(self):
        stdin = Entermsg.get()
        Entermsg.delete(0,END)
        
        request = 'FROM %s: %s\r\n' % (self.user, stdin)
        
        self.sock.send(request.encode(encoding='UTF-8'))
        if self.debug:
            mylist.insert(END, '>' + str(request) + '')
    
    def Quitgoing(self):
        request = 'QUIT\r\n'
        if self.debug is True:
            mylist.insert(END, '> QUIT')
        self.sock.send(request.encode(encoding='utf_8'))
        time.sleep(1)
        '''
        self.mainconsole.quit()
        '''
        self.mainconsole.destroy()
        
    def login(self):
        request = 'USER'
        self.user = Users['name'].get()
        self.password = Users['password'].get()
        userInfo = '%s %s\r\n' % (request, self.user)
        self.sock.send(userInfo.encode(encoding='utf_8'))
        
    
    def Responsemsg(self, response):
        global mylist
        words = response.split(None, 1)
        if (not words[0].isdigit()):
            mylist.insert(END, 'Illegal command: %s' % (response))
            return
        code = int(words[0])
        if self.debug or code >= 300 or code < 200:
            mylist.insert(END, '<', str(response))
        if code == 299 or code == 231:
            out = words[1].split(None, 1)
            if len(out) < 2:
                mylist.insert(END,'')
            else:
                mylist.insert(END,str(out[1]))
                
    def dispatch(self):
        global mylist
        while True:
            if self.debug: 
                time.sleep(1)
            response = self.sock.recv(1024).decode()
            if response:
                for rmg in response.split('\r\n'):
                    if rmg:
                        self.Responsemsg(rmg)
            
if __name__ == '__main__':
    serverHost = '127.0.0.1'
    serverPort = 9629
    client = ChatClient(serverHost, serverPort)
    threading._start_new_thread(client.dispatch,())
    client.index.mainloop()