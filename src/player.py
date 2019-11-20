from src.hand import hand
from src.config import config
from random import randint

class player:
    strats = ["basic", "standat17", "drunk"]

    def __init__(self, pos, dealer, comp):
        self.isComp = comp
        if comp:
            self.strat = self.strats[randint(0, 2)]
        if dealer:
            self.state = "idle"
        else:
            self.money = config["setup"]["start money"]
            self.state = "playing"
        self.pos = pos
        self.hand = hand()
