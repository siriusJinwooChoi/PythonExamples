# -*- coding: utf-8 -*-

from card import BJCard, Deck
 
class BJCards(list):
    """Blackjack Cards Class
    Attributes:
        possible_sums: all the possible sum of card
        hand: -1 if bust
              highest sum of possible sums, otherwise
    """
    def __init__(self):
        list.__init__(self)
        self.possible_sums = set([0])   # init possible sums (== 0)
        self.hand = 0                   # hand of BJCards. -1 if bust
    def hit(self, card):
        """Hit a BJcard and append it. 
        Then, find all possible sums and the current hand.
        The current hand is defined as max. of possible sums
        The current hand should be -1 if burst"""
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
        """Is current cards the Blackjack?"""
        if self.hand == 21 and len(list(self)) ==2:
            print '%s = Blackjack'%self
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
        return "BJCards(%s) = %s" % (list(self),self.possible_sums)
    
class Player:
    """Player class
    Attributes:
        name: player's name
        init_budget: initial budget
        budget: current budet
        game: game joined by the player
        cards: BJ Cards given to the player
        state: 'active', 'stand', or 'burst'
    """
    def __init__(self, name, budget,state =None):
        self.name =name
        self.budget = budget
        self.restart()
    def restart(self):
        """Restart another round.
        Check the remaining budget and leave the game if budget <= 0.
        Create new BJCards"""
        self.state ='active'
        if self.budget <= 0:
            return self.leave()
        self.cards =BJCards()
        self.bet_amount =0
        
    def join(self, game):
        """join the Blackjack game"""
        self.game = game
        self.game.join(self)
        return self.game
    def leave(self):
        """Leave the Blackjack game"""
        self.game.leave(self)
        return self.game
    def bet(self, amount):
        """Bet the amount of money.
        Cannot exceed player's budget"""
        if amount >self.budget:
            print 'you cannot bet because of little money'
        else:
            self.bet_amount = amount
            print 'you bet %s' % (amount)
            
    def hit(self, card):
        """Hit a card and check if bust"""
        self.cards.hit(card)
        if self.cards.hand ==-1:
            self.state ='burst'
    def stand(self):
        self.state ='stand'
        
    def __repr__(self):
        """Represent in the form as: name, state: repr(BJCards)"""  
        return 'name:%s ,state :%s,%s' % (self.name, self.cards,self.state)
        
class Dealer(Player):
    """Dealer is a player competing against players in the game. 
    Dealer has a card deck and deals players cards
    Attributes:
        deck: a deck of BJCard
    """
    def __init__(self):
        Player.__init__(self, name='dealer', budget=1000000)
        self.deck=Deck(BJCard)
    def __repr__(self):
        """Represent in the form as: name, state: repr(BJCards)
        2nd card in BJCards object should be makred as '?' to hide the face        
        """
        return 'name:%s ,state :%s,%s' % (self.name, self.cards,self.state)
    def get_card(self):
        """Get a card from the deck"""
        return self.deck.pop()
    def join(self, game):
        """join a Blackjack game"""
        self.game = game
        self.game.dealer_join(self)
        return self.game
    def leave(self):
        """Leave the Blackjack game"""
        self.game.dealer_leave(self)
        return self.game
    def showdown(self):
        """Face up dealer's hidden card and balance with players in the game"""
        print "%s: %s" %(self.name, repr(self.cards))     # open dealer's cards
        for player in self.game.players:
            win = self.balance(player)
            if win > 0: 
                print player.name, 'wins', win
            elif win == 0: 
                print player.name, 'draws'
            elif win <0:
                print player.name, 'loses', -(win)   
            self.budget -= win
            player.budget += win
            print 'budget of %s : %s'%(player.name,player.budget)
            print 'budget of %s : %s'%(self.name,self.budget)
    def balance(self, player):
        """Who wins? Caculate pay-back according to player's betting amount.
        Returns:
            positive amount if player wins
            0 if draw
            negative amount if player loses
        """
        print 'hand of %s: %s'%(player.name,player.cards.hand)
        print 'hand of %s: %s'%(self.name,self.cards.hand)
        if player.cards.hand == self.cards.hand:
            return 0
        elif player.cards.hand > self.cards.hand:
            return player.bet_amount*2
        else:
            return -player.bet_amount
    def deal(self):
        # player's betting first
        for player in self.game.players:
            amount = self.__ask_bet(player)
            player.bet(amount)
        # turn down first two cards
        for i in range(2):
            for player in self.game.players:
                player.hit(self.get_card())
                print player
            self.hit(self.get_card())
            print self
        # deal next cards    
        if not self.cards.is_blackjack():
            print "players' turn:"
            for player in self.game.players:
                while player.state == 'active' :
                    self.deal_player(player)
                    print player
            print "dealer's turn:"
            while self.state == 'active':
                self.deal_self()
                print self
        # Who wins?
        self.showdown()        
    def deal_player(self, player):
        """Player can choose hit or stand""" 
        answer = self.__ask_hit_or_stand(player)
        if answer in ('hit'):
            player.hit(self.get_card())
        elif answer in('stand'):
            player.stand()
    def deal_self(self):
        """Dealer have no choice. Stand if hand >= 17, otherwise hit"""
        self.cards.hit(self.get_card())
        if self.cards.hand < 17 and self.cards.hand>=0:
            self.state = 'active'
        elif self.cards.hand >= 17 and self.cards.hand <= 21:
            self.state = 'stand'
        elif self.cards.hand==-1:
            self.state = 'burst'
    def __ask_hit_or_stand(self, player):
        while True:
            answer = raw_input('> %s, hit or stand? ' % player.name)
            if answer in ('h', 'hit'):
                return 'hit'
            elif answer in ('s', 'stand'):
                return 'stand'    
    def __ask_bet(self, player):
        while True:
            try:
                amount = int(raw_input('> %s, how much want to bet? (%d) ' \
                        %(player.name, player.budget)))
            except Exception as e:
                print e
            else:
                return amount

class BJGame:
    
    """Blackjack game consist of a dealer, one or more players    
    """
    Round =0
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
    print "==Testing BJCards"
    def test_cards(card_list):
        cards = BJCards()
        for c in card_list:
            cards.hit(BJCard(c))
        print cards
        print cards.hand
        return cards
        
    bob_cards = BJCards()
    sue_cards = BJCards()
    tom_cards = BJCards()
    bob_cards = test_cards(['KD', '8S', '2D'])
    assert bob_cards.hand == 20
    sue_cards = test_cards(['9S', '5S', 'JD', 'TS'])
    assert sue_cards.hand == -1  # bust
    tom_cards = test_cards(['QC', 'AH']) 
    assert tom_cards.hand == 21
    assert sue_cards < bob_cards < tom_cards
    assert tom_cards > test_cards(['9C', '7S', '5C'])
    
    print "==Testing Player"
    game = BJGame()
    bob = Player('bob', 100)
    bob.join(game)
    bob.bet(10); bob.hit(BJCard('KD')); bob.hit(BJCard('8S')); bob.hit(BJCard('2D')); bob.stand()
    print bob
    
    print "== Testing Dealer"
    dealer = Dealer()
    dealer.join(game)
    while dealer.state == 'active':
        dealer.deal_self()
        print dealer
    print dealer
    bob.restart()
    dealer.restart()
    dealer.deal()
    
    print "== Run BJGame"
    game = BJGame()
    dealer = Dealer()
    dealer.join(game)
    bob = Player('bob', 100)
    bob.join(game)
    tom = Player('tom', 200)
    tom.join(game)
    game.start()
    game.start()
#    game.repeat()

    print '==Run BjGame including me'
    game = BJGame()
    dealer = Dealer()
    dealer.join(game)
    MinGeun =Player('MinGeun', 1000)
    MinGeun.join(game)
    bob = Player('bob', 100)
    bob.join(game)
    tom = Player('tom', 200)
    tom.join(game)
    game.repeat()
