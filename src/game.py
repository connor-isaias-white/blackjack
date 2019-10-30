import pygame
from src.config import config
from src.deck import deck
from src.player import player
from random import randint

class Game:
    def __init__(self, display):
        pygame.init()
        self.display = display
        self.running = True
        self.font = pygame.font.Font('assets/FiraCode.ttf', 42)
        self.players =[]
        self.turn = 0

    def loop(self):
        shoe = deck(5)
        shoe.shuffle()
        clock = pygame.time.Clock()
        self.setupPlayers()

        self.deal(shoe)
        while self.running:
            self.events(shoe)
            pygame.display.update()
            clock.tick(config['game']['fps'])

    def events(self, shoe):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.hit(self.turn % len(self.players), shoe)
                    self.turn +=1

    def setupPlayers(self):
        for i in range(config["setup"]["players"]):
            Player = player(i)
            self.players.append(Player)

    def hit(self, Player,shoe):
        self.players[Player].hand.addCard(shoe.shoe[0])
        cardplace = self.players[Player].hand.numCards
        self.showcard(shoe.shoe[0], (Player+1)/(len(self.players)+1)*config["game"]['width']+5.2*[0,12,6,-6][cardplace % 4]*2, config["game"]['height']*(0.9-(int(cardplace/2))*0.134))
        shoe.shoe.pop(0)

    def deal(self, shoe):
        for i in range(len(self.players)*2):
            self.players[i % len(self.players)].hand.addCard(shoe.shoe[0])
            self.showcard(shoe.shoe[0], ((i % len(self.players))+1)/(len(self.players)+1)*config["game"]['width']+5.2*12*(int(i/(len(self.players)))), config["game"]['height']*(0.9-(int(i/(len(self.players))))*0.134))
            shoe.shoe.pop(0)

    def showcard(self, card, xshift, yshift):
        size = 12
        xshift = xshift-6*size
        yshift = yshift-6*size
        pygame.draw.polygon(self.display,config["colours"]["white"],[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
        text = self.font.render(card.uni+card.apperance+card.uni, True,config["colours"][card.colour], config["colours"]["white"])
        textRect = text.get_rect()
        textRect.center = (xshift+6*size, yshift+6*size)
        self.display.blit(text, textRect)
