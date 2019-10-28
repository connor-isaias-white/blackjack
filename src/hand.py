class hand:

    def __init__(self):
        self.numCards= 0
        self.total = 0
        self.cards = []
        self.soft = False

    def addCard(self, card):
        self.cards.append(card)
        self.total += card.value
        if card.isAce:
            self.soft = True
