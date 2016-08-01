# -*- coding: utf-8 -*-
import sys, socket
import os
from Tkinter import *
from tkMessageBox import *

class Blackjack:
    def __init__(self): 

        self.root = Tk()
        
        '''
        self.two_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card0.gif")
        self.three_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card1.gif")
        self.four_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card2.gif")
        self.five_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card3.gif")
        self.six_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card4.gif")
        self.seven_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card5.gif")
        self.eight_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card6.gif")
        self.nine_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card7.gif")
        self.ten_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card8.gif")
        self.j_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card9.gif")
        self.q_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card10.gif")
        self.k_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card11.gif")
        self.a_c = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card12.gif")
        
        self.two_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card13.gif")
        self.three_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card14.gif")
        self.four_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card15.gif")
        self.five_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card16.gif")
        self.six_ = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card17.gif")
        self.seven_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card18.gif")
        self.eight_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card19.gif")
        self.nine_d= PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card20.gif")
        self.ten_d= PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card21.gif")
        self.j_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card22.gif")
        self.q_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card23.gif")
        self.k_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card24.gif")
        self.a_d = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card25.gif")
        
        self.two_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card26.gif")
        self.three_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card27.gif")
        self.four_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card28.gif")
        self.five_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card29.gif")
        self.six_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card30.gif")
        self.seven_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card31.gif")
        self.eight_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card32.gif")
        self.nine_h= PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card33.gif")
        self.ten_h= PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card34.gif")
        self.j_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card35.gif")
        self.q_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card36.gif")
        self.k_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card37.gif")
        self.a_h = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card38.gif")
        
        self.two_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card39.gif")
        self.three_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card40.gif")
        self.four_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card41.gif")
        self.five_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card42.gif")
        self.six_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card43.gif")
        self.seven_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card44.gif")
        self.eight_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card45.gif")
        self.nine_s= PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card46.gif")
        self.ten_s= PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card47.gif")
        self.j_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card48.gif")
        self.q_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card49.gif")
        self.k_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card50.gif")
        self.a_s = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/card51.gif")
        self.back = PhotoImage(file="C:/Users/Jung/Desktop/cardimages/back-red.gif")
        '''
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost",8121))
        money = 1000
        '''def change(mes):
    spt = mes
    k = spt.split("([",1)
    final=k[1].rsplit("])",1)
    final_lst = final[0].split(", ")'''

        def bet_fields():
            #처음에는 카드가 안 보이는 상황에서 돈을 배팅
            sock.send(self.e1.get()) #돈을 보냄
            flag=0
            while flag < 2:
                    curstate = sock.recv(1024)

                    print curstate
                    flag += 1
                    
            self.q.config(text="Hit or Stand")
            self.e1.delete(0,END)
            
        def stand_fields():
            sock.send("stand")
            
            self.q.config(text="How much?")
            
   
        def hit_fields():
            sock.send("hit")
            card = sock.recv(1024)
            print card
            if card[0:14] == 'player was bursted':
                self.q.config(text="How much?")
             
        def print_entry_fields():
            showerror('Error','close?')
            self.root.destroy()
            
        self.frame = Frame(self.root,bg='darkgreen', width=1000,height=1000)
        
        self.frame.pack()

        hh='4h'
        #hh==self.four_h
        Label(self.frame, text="BlackJack\n", fg = "white", bg = 'darkgreen', font = "Verdana 30 bold").pack()
       
        self.q = Label(self.frame, fg = 'white', text = 'how much?',bg = 'darkgreen',font = "Verdana 15 ")
        self.q.pack()
        self.e1 = Entry(self.frame)
        self.e1.pack()
        
        self.stop = Button(self.frame, text='Stop',activeforeground = 'white', activebackground = 'red',width = 10,command=print_entry_fields)
        self.stop.pack(side = 'right', padx = 10, pady=10)                

        self.bet = Button(self.frame, text='bet',activeforeground = 'white', activebackground = 'blue',width = 10 , command=bet_fields)
        self.bet.pack(side = 'right', padx = 5, pady=10)
        
        self.hit = Button(self.frame, text='hit',activeforeground = 'white', activebackground = 'yellow',width = 10 , command=hit_fields)
        self.hit.pack(side = 'left', padx = 5, pady=10)
        self.stand = Button(self.frame, text='stand',activeforeground = 'white', activebackground = 'purple',width = 10 , command=stand_fields)
        self.stand.pack(side = 'left', padx = 5, pady=10)


        self.frame.mainloop()
        

if __name__=="__main__":
    Blackjack()
