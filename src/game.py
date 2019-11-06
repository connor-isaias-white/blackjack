import pygame
from src.config import config
from src.deck import deck
from src.player import player
from random import randint
from src.hand import hand

class Game:
    def __init__(self, display):
        pygame.init()
        self.display = display
        self.running = True
        self.done = 0
        self.turn = 0
        self.font = pygame.font.Font('assets/FiraCode.ttf', 42)
        self.players =[]

    def loop(self):
        self.shoe = deck(5)
        self.shoe.shuffle()
        clock = pygame.time.Clock()
        self.setupPlayers()
        self.roundSetup()

        while self.running:
            print(self.players[self.turn % len(self.players)].state)
            if self.done == len(self.players):
                self.roundend()
            elif self.players[self.turn % len(self.players)].state != "playing":
                self.turn +=1
            self.events()
            pygame.display.update()
            clock.tick(config['game']['fps'])

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.hit(self.turn % len(self.players))
                    self.turn +=1
                elif event.key == pygame.K_s:
                    self.stand(self.turn % len(self.players))
                    self.turn +=1

    def setupPlayers(self):
        for i in range(config["setup"]["players"]):
            Player = player(i)
            self.players.append(Player)

    def roundSetup(self):
        self.turn = 0
        self.done = 0
        for i in range(len(self.players)*2):
            self.hit(i % len(self.players))


    def stand(self, Player):
        self.players[Player].state = "stopped"
        self.done +=1

    def bust(self, Player):
        self.players[Player].state = "busted"
        self.done +=1

    def hit(self, Player):
        if (self.players[Player].hand.total < 21):
            self.players[Player].hand.addCard(self.shoe.shoe[0])
            cardplace = self.players[Player].hand.numCards
            if  self.players[Player].hand.total > 21:
                if self.players[Player].hand.numaces > 0:
                    self.players[Player].hand.numaces -= 1
                    self.players[Player].hand.soft = False
                    self.players[Player].hand.total -= 10
                else:
                    self.bust(Player)
            self.showcard(self.shoe.shoe[0], (Player+1)/(len(self.players)+1)*config["game"]['width']+5.2*[0,12,6,-6][cardplace % 4]*2, config["game"]['height']*(0.9-(int(cardplace/2))*0.134), Player)
            self.shoe.shoe.pop(0)


    def roundend(self):
        for i in self.players:
            print(i.hand.total)
        i.hand = hand()
        self.roundSetup(self.shoe)

    def showcard(self, card, xshift, yshift, Player):
        size = 12

        xshift = xshift-6*size
        yshift = yshift-6*size
        pygame.draw.polygon(self.display,config["colours"]["white"],[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
        text = self.font.render(card.uni+card.apperance+card.uni, True,config["colours"][card.colour], config["colours"]["white"])
        textRect = text.get_rect()
        textRect.center = (xshift+6*size, yshift+6*size)
        self.display.blit(text, textRect)

        xshift = (Player+1)/(len(self.players)+1)*config["game"]['width']-6*size
        yshift = config["game"]['height']*(0.9)-6*size
        pygame.draw.polygon(self.display,config["colours"]["white"],[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
        text = self.font.render(str(self.players[Player].hand.total), True,config["colours"]["green"], config["colours"]["white"])
        textRect = text.get_rect()
        textRect.center = (xshift+6*size, yshift+6*size)
        self.display.blit(text, textRect)
