from src.hand import hand
from src.config import config
class player:

    def __init__(self, pos, dealer, comp):
        self.isComp = False
        if dealer:
            self.state = "idle"
        else:
            self.money = config["setup"]["start money"]
            self.state = "playing"
        self.pos = pos
        self.hand = hand()
