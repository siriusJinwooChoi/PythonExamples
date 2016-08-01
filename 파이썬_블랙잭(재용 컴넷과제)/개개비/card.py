# -*- coding: utf-8 -*-

SUITS = 'CDHS'
RANKS = '23456789TJQKA'

class Card:
    """Poker card class
    """
    VALUES =dict(zip(RANKS, range(2,2+len(RANKS))))
    
    def __init__(self, rank, suit=None):
        if suit == None:
            if len(rank) !=2:raise ValueError('Invaild card')
            self.rank,self.suit =rank
        else:
            self.rank, self.suit =rank,suit
        if self.rank not in RANKS or self.suit not in SUITS:
            raise ValueError('Invaild card')
        
    def value(self):
        return Card.VALUES[self.rank]
    
    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__,self.rank + self.suit)
    def __gt__(self,other):
        return self.value() >other.value()
    def __lt__(self,other):
        return self.value()<other.value()
    def __eq__(self,other):
        return self.value()==other.value()
    def __getitem__(self,index):
        if index == 0 :
            return self.rank
        elif index == 1 :
            return self.suit
        else:
            raise IndexError
    def __setitem__(self,index,value):
        if index == 0:
            self.rank =value
        elif index==1 :
            self.suit= value
        else:
            raise IndexError
    
class BJCard(Card):
    """Blackjack card class
    """
    VALUES = dict(zip(RANKS, [2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 0, 0, 1]))
    def value(self):
        return BJCard.VALUES[self.rank]
    
import random

class Deck(list):
    """A Deck of Cards
    """
    def __init__(self,cls):
        list.__init__(self)
        for i in RANKS:
            for j in SUITS:
                self.append(cls(i,j))
        self.cls =cls
        self.shuffle()
    def shuffle(self):
        random.shuffle(self)
    def pop(self):
        """Get a card from top of the deck
        Should create new deck and shuffle it if empty
        """
        if self == []:
            print 'another deck of card'
            self = Deck(self.cls)
            self.shuffle()
        return list.pop(self)
       
if __name__ == '__main__':    
    print "== Testing Card class"    
    c1 = Card('Q', 'C')
    c2 = Card('9C')
    c3 = Card('9D')
    print c1, c2, c3
    assert c1 > c2
    assert c2 == c3
    
    print "==Testing BJCard class"
    c1 = BJCard('Q', 'C')
    c2 = BJCard('KC')
    c3 = BJCard('AD')
    print c1, c2, c3
    assert c1 == c2
    assert c2 < c3
    c_list = [BJCard(c) for c in ['2D', 'KS', 'TD', 'AC', 'KD']]
    assert [c.value() for c in c_list] == [2, 0, 10, 1, 0]
    c_list.sort()
    print c_list
    
    print "== Testing Deck"
    deck = Deck(BJCard)
    print deck
    for i in range(60):
        print deck.pop()

    
    
