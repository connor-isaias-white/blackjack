from src.hand import hand
class player:

    def __init__(self, pos, dealer):
        self.isComp = False
        if dealer:
            self.state = "idle"
        else:
            self.money = 1000
            self.state = "playing"
        self.pos = pos
        self.hand = hand()
