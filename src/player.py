from src.hand import hand
from src.config import config
from random import randint

class player:
    strats = ["basic", "standat17", "rand"]

    def __init__(self, pos, dealer, comp, strat):
        self.isComp = comp
        if comp:
            self.strat = strat
            if self.strat == "any":
                self.strat = self.strats[randint(0, 2)]
        if dealer:
            self.state = "idle"
        else:
            self.money = config["setup"]["start money"]
            self.state = "playing"
        self.pos = pos
        self.hand = hand()
