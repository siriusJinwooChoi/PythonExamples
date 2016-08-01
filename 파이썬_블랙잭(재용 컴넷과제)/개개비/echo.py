import sys, socket

def client(server_addr):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    money = 1000
    while True:
        asking = sock.recv(1024)
        print asking
        message = sys.stdin.readline() #µ·
        sock.send(message) #µ·
        flag = 0
        while True:
            while flag < 2:
                curstate = sock.recv(1024)
                print "BJCards = %s" %curstate
                flag += 1
                
            quest = sock.recv(1024)
            print quest
            message1=sys.stdin.readline() #h, s
            sock.send(message1)
            if message1 == 'h\n':           #if player hit
                card = sock.recv(1024)      #card -> player's state(check the burst)
                if card == 'player was bursted':        #if burst
                    print card
                    
                    phandof = sock.recv(1024)
                    dhandof = sock.recv(1024)
                    money = sock.recv(1024)
                    pbudget = sock.recv(1024)
                    dbudget = sock.recv(1024)
                    
                    print phandof
                    print dhandof
                    print ("money:", int(money))
                    print pbudget
                    print dbudget
                    
                    break
                
                else:                                   #if not burst
                    print ("BJCards() = %s" %(card))
            #'card = sock.recv(1024) '
                
            if message1 == 's\n':           #if player stand
                cmd = sock.recv(1024)
                
                phandof = sock.recv(1024)
                dhandof = sock.recv(1024)
                money = sock.recv(1024)
                pbudget = sock.recv(1024)
                dbudget = sock.recv(1024)
                
                print phandof
                print dhandof
                print ("money:", int(money))
                print pbudget
                print dbudget
                
                break
            #'print card' #¿ì¸® ÆÐ
    sock.close()
    print 'close'
    
if __name__=='__main__':
    client(('localhost', 9629))
