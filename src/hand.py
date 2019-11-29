class hand:

    def __init__(self):
        self.numCards= 0
        self.total = 0
        self.cards = []
        self.numaces = 0

    def addCard(self, card):
        self.cards.append(card)
        self.numCards += 1
        if card.isAce:
            self.numaces += 1
        self.total += card.value
        if  self.total > 21:
            if self.numaces > 0:
                self.numaces -= 1
                self.total -= 10
