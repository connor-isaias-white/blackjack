from src.card import card
from random import randint

class deck:
    suits= ["Heart", "Spade", "Club", "Diamond"]
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, numDecks):
        self.numDecks = numDecks
        self.shoe = []
        self.cutCard = randint((numDecks*52)*3/4, numDecks*52-13)
        for num in range(numDecks):
            for suit in self.suits:
                for cardname in self.cards:
                    Card = card(suit, cardname, num)
                    self.shoe.append(Card)

    def shuffle(self):
        for i in range(100000):
            old = randint(0, self.numDecks*52-1)
            new =randint(0, self.numDecks*52-1)
            if old != new:
                temp = self.shoe[new]
                self.shoe[new] = self.shoe[old]
                self.shoe[old]= temp

    def printdeck(self):
        for i in self.shoe:
            print(f"{i.name} of {i.suit}s, deck: {i.deck}")
