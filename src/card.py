class card:
    cardTypes = {
    "2": {"value":2, "isAce": False, "apperance": "2"},
    "3": {"value":3, "isAce": False, "apperance": "3"},
    "4": {"value":4, "isAce": False, "apperance": "4"},
    "5": {"value":5, "isAce": False, "apperance": "5"},
    "6": {"value":6, "isAce": False, "apperance": "6"},
    "7": {"value":7, "isAce": False, "apperance": "7"},
    "8": {"value":8, "isAce": False, "apperance": "8"},
    "9": {"value":9, "isAce": False, "apperance": "9"},
    "10": {"value":10, "isAce": False, "apperance": "10"},
    "Jack": {"value":10, "isAce": False, "apperance": "J"},
    "King": {"value":10, "isAce": False, "apperance": "Q"},
    "Queen": {"value":10, "isAce": False, "apperance": "K"},
    "Ace": {"value":11, "isAce": True, "apperance": "A"}
    }
    suits={
        "Diamond":{"colour":"red", "uni":u"\u25C6"},
        "Heart":{"colour":"red", "uni":u"\u2665"},
        "Spade":{"colour":"black", "uni":u"\u2660"},
        "Club":{"colour":"black", "uni":u"\u2663"},
    }

    def __init__(self, suit, name, deck):
        self.name = name
        self.value = self.cardTypes[name]["value"]
        self.isAce = self.cardTypes[name]["isAce"]
        self.apperance = self.cardTypes[name]["apperance"]
        self.suit = suit
        self.colour = self.suits[suit]["colour"]
        self.uni = self.suits[suit]["uni"]
        self.deck = deck
