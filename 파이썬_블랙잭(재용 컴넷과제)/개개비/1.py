# -*- coding: utf-8 -*-
from card import BJCard, Deck
from socket import socket, AF_INET, SOCK_STREAM

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', 9629))
sock.listen(5)
conn, addr=sock.accept()

class BJCards(list):
    def __init__(self):
        list.__init__(self)
        self.possible_sums = set([0])   # init possible sums (== 0)
        self.hand = 0                   # hand of BJCards. -1 if bust
    def hit(self, card):
        self.append(card)
        values=[]
        values.append(card.value())
        if values[0] < 2:
            values.append(values[0]+ 10)
        new_sums =set([v+s for v in values for s in self.possible_sums if v+s <=21])
        new_sums =sorted(new_sums)
        if len(new_sums) ==0:
            self.hand=-1
        else:
            self.hand = new_sums[-1]
        self.possible_sums = new_sums              
    def is_blackjack(self):
        if self.hand == 21 and len(list(self)) ==2:
            bjcard = '%s = Blackjack'%self
            print bjcard
            return True
    def __lt__(self, other):
        if other.is_blackjack():
            return -1
        else:
            return self.hand<other.hand
    def __gt__(self, other):
        if self.is_blackjack():
            return 1
        else:
            return self.hand>other.hand
    def __eq__(self, other):
        if not self.is_blackjack() and not other.is_blackjack():
            return self.hand == other.hand
    def __repr__(self):
        BJStates = "BJCards(%s) = %s" % (list(self),self.possible_sums)
        return BJStates
    
class Player:
    def __init__(self, name, budget, state = None):
        self.name = name
        self.budget = budget
        self.restart()
    def restart(self):
        self.state = 'active'
        if self.budget <= 0:
            return self.leave()
        self.cards = BJCards()
        self.bet_amount = 0       
    def join(self, game):
        self.game = game
        self.game.join(self)
        return self.game
    def leave(self):
        self.game.leave(self)
        return self.game
    def bet(self, amount):
        if amount < self.budget:
            print 'you cannot bet because of little money'
        else:
            self.bet_amount = amount
            print 'you bet %s' % (amount)
    def hit(self, card):
        self.cards.hit(card)
        if self.cards.hand ==-1:        #current state == burst
            self.state ='burst'
        #imsi = str(self.cards)
        #conn.send(imsi)
    def stand(self):
        self.state ='stand' 
    def __repr__(self):
        playerstate = 'name:%s ,state :%s,%s' % (self.name, self.cards, self.state)
        if self.state == 'burst':
            plburst = 'player was bursted'
            conn.send(plburst)
        else:
            conn.send(str(self.cards))
        return playerstate
        
class Dealer(Player):
    def __init__(self):
        Player.__init__(self, name='dealer', budget=1000000)
        self.deck=Deck(BJCard)
    def __repr__(self):
        dealerstate = 'name:%s ,state :%s,%s' % (self.name, self.cards, self.state)
        return dealerstate
    def get_card(self):
        return self.deck.pop()
    def join(self, game):
        self.game = game
        self.game.dealer_join(self)
        return self.game
    def leave(self):
        self.game.dealer_leave(self)
        return self.game
    def showdown(self):
        print "%s: %s" %(self.name, repr(self.cards))     # open dealer's cards
        for player in self.game.players:
            win = self.balance(player)
            if win > 0:
                print player.name, 'wins', win
            elif win == 0: 
                print player.name, 'draws'
            elif win < 0:
                print player.name, 'loses', -(win)   
            self.budget -= win
            player.budget += win

            pbudget = 'budget of %s : %s ****'%(player.name, player.budget)
            dbudget = 'budget of %s : %s'%(self.name,self.budget)
            print pbudget
            print dbudget
            conn.send(str(player.budget))
            conn.send(pbudget)
            conn.send(dbudget)
            
    def balance(self, player):
        phandof = 'hand of %s: %s'%(player.name,player.cards.hand)
        dhandof = 'hand of %s: %s'%(self.name,self.cards.hand)
        
        print phandof
        print dhandof

        conn.send(phandof)
        conn.send(dhandof)
        
        if player.cards.hand == self.cards.hand:
            return 0
        elif player.cards.hand > self.cards.hand:
            return int(player.bet_amount)
        else:
            return -int(player.bet_amount)
        
    def deal(self):
        for player in self.game.players:
            amount = self.__ask_bet(player)
            player.bet(amount)
        for i in range(2):
            for player in self.game.players:
                player.hit(self.get_card())
                print player
            self.hit(self.get_card())
            print self
        if not self.cards.is_blackjack():
            print "players' turn:"
            #imsi = str(player.cards)
            #conn.send(imsi)
            for player in self.game.players:
                while player.state == 'active' :
                    self.deal_player(player)
                    print player
            print "dealer's turn:"
            while self.state == 'active':
                self.deal_self()
                print self
        self.showdown()        
    def deal_player(self, player):
        answer = self.__ask_hit_or_stand(player)
        if answer in ('hit'):
            player.hit(self.get_card())
        elif answer in('stand'):
            player.stand()
    def deal_self(self):
        self.cards.hit(self.get_card())
        if self.cards.hand < 17 and self.cards.hand>=0:
            self.state = 'active'
        elif self.cards.hand >= 17 and self.cards.hand <= 21:
            self.state = 'stand'
        elif self.cards.hand==-1:
            self.state = 'burst'
        
    def __ask_hit_or_stand(self, player):
        while True:
            quest = '> %s, hit or stand? ' % player.name 
            print quest
            conn.send(quest)
            
            answer=conn.recv(1024)
            if answer in ('h\n', 'hit'):
                if answer[-1] == '\n':
                    answer = answer.replace('\n', '')
                return 'hit'
            elif answer in ('s\n', 'stand'):
                if answer[-1] == '\n':
                    answer = answer.replace('\n', '')
                #conn.send(str(player.budget))
                return 'stand'    
    def __ask_bet(self, player):
        while True:
            try:
                ask = '> %s, how much want to bet? (%d) ' %(player.name, player.budget)
                print ask
                conn.send(ask)
                temp = conn.recv(1024)
                if temp[-1] == '\n':
                    amount = temp.replace('\n', '')
                
            except Exception as e:
                print e
                break
            else:
                return amount

class BJGame:
    Round = 0
    def __init__(self):
        self.players = []
        self.dealer = None
    def join(self, player):
        self.players.append(player)
    def leave(self, player):
        self.players.remove(player)
    def dealer_join(self, dealer):
        self.dealer = dealer
    def dealer_leave(self, dealer):
        self.dealer = None
    def start(self):
        if not self.players: 
            print 'No players on the table'
            return False
        if self.dealer == None:
            print 'Dealer lost all the money. No dealer present'
            return False 
        print 'Starting round'
        self.dealer.deal()
        # Prepare to restart
        for player in self.players[:]:
            player.restart()
        self.dealer.restart()
        return True
    def repeat(self):
        while self.start():
            pass            
           
if __name__ == '__main__':
    print '==Run=='
    game = BJGame()
    print 1
    dealer = Dealer()
    print 2
    dealer.join(game)
    print 3
    StepUp = Player('StepUp', 1000)
    print 4
    StepUp.join(game)
    print 5
    game.repeat()
    print 6
