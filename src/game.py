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
        self.shoe = deck(10)
        self.shoe.shuffle()
        clock = pygame.time.Clock()
        self.setupPlayers()
        self.roundSetup()

        while self.running:
            if self.done == len(self.players):
                self.roundend()
            elif self.players[self.turn % len(self.players)].state != "playing":
                #self.showcards(self.turn % len(self.players), config["colours"]["dark gray"])
                self.turn +=1
            else:
                self.showcards(self.turn % len(self.players), config["colours"]["white"])
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
        self.display.fill(config["colours"]["black"])
        self.turn = 0
        self.done = 0
        for i in range(len(self.players)*2):
            self.hit(i % len(self.players))


    def stand(self, Player):
        self.players[Player].state = "stopped"
        self.showcards(Player, config["colours"]["dark gray"])
        self.done +=1

    def bust(self, Player):
        self.players[Player].state = "busted"
        self.showcards(Player, config["colours"]["dark gray"])
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
            elif self.players[Player].hand.total == 21:
                self.stand(Player)
            else:
                self.showcards(Player, config["colours"]["gray"])
            self.shoe.shoe.pop(0)


    def roundend(self):
        for i in self.players:
            print(i.hand.total)
            i.hand = hand()
            i.state = "playing"
        self.roundSetup()

    def showcards(self, Player,colour):
        size = 12

        # cards
        for i in range(len(self.players[Player].hand.cards)):
            card = self.players[Player].hand.cards[i]
            xshift = (Player+1)/(len(self.players)+1)*config["game"]['width']+5.2*[12,6,-6,0][i % 4]*2 -6*size
            yshift = config["game"]['height']*(0.9-(int((i+1)/2))*0.134)-6*size

            pygame.draw.polygon(self.display,colour,[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
            text = self.font.render(card.uni+card.apperance+card.uni, True,config["colours"][card.colour], colour)
            textRect = text.get_rect()
            textRect.center = (xshift+6*size, yshift+6*size)
            self.display.blit(text, textRect)
        #total
        xshift = (Player+1)/(len(self.players)+1)*config["game"]['width']-6*size
        yshift = config["game"]['height']*(0.9)-6*size
        pygame.draw.polygon(self.display,colour,[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
        text = self.font.render(str(self.players[Player].hand.total), True,config["colours"]["green"], colour)
        textRect = text.get_rect()
        textRect.center = (xshift+6*size, yshift+6*size)
        self.display.blit(text, textRect)
