from src.hand import hand
class player:

    def __init__(self, pos):
        self.isComp = False
        self.pos = pos
        self.money = 1000
        self.hand = hand()
