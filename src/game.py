import pygame
from src.config import config
from src.deck import deck
from src.player import player
from random import randint
from src.hand import hand
from src.basic import basic
from time import sleep

class Game:
    def __init__(self, display):
        pygame.init()
        self.display = display
        self.running = True
        self.done = 0
        self.turn = 0
        self.font = pygame.font.Font('assets/FiraCode.ttf', 42)
        self.players =[]
        self.dealer = player(config["setup"]["players"]+1, True, True)

    def loop(self):
        self.shoe = deck(10)
        self.shoe.shuffle()
        clock = pygame.time.Clock()
        self.setupPlayers()
        self.roundSetup()

        while self.running:
            if self.done == len(self.players):
                self.dealerturn()
            elif self.players[self.turn % len(self.players)].state != "playing":
                self.turn +=1
            elif self.players[self.turn % len(self.players)].isComp:
                self.compmove(self.turn % len(self.players))
                self.turn +=1
            else:
                self.showCards(self.turn % len(self.players), config["colours"]["white"])
                self.last = pygame.time.get_ticks()
            self.events()
            pygame.display.update()
            clock.tick(config['game']['fps'])

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                exit()
            elif event.type == pygame.KEYDOWN:
                if self.players[self.turn % len(self.players)].isComp == False:
                    if event.key == pygame.K_h:
                        self.hit(self.turn % len(self.players))
                        self.turn +=1
                    elif event.key == pygame.K_s:
                        self.stand(self.turn % len(self.players))
                        self.turn +=1

    def setupPlayers(self):
        for i in range(config["setup"]["players"]):
            if i = int(config["setup"]["players"])/2:
                Player = player(i, False, False)
            else:
                Player = player(i, False, True)
            self.players.append(Player)

    def roundSetup(self):
        self.display.fill(config["colours"]["black"])
        self.turn = 0
        self.done = 0
        for i in range(len(self.players)*2):
            self.hit(i % len(self.players))

        for i in range(2):
            self.dealer.hand.addCard(self.shoe.shoe[0])
            self.shoe.shoe.pop(0)
        self.showDealercards(False)


    def stand(self, Player):
        self.players[Player].state = "stopped"
        self.showCards(Player, config["colours"]["dark gray"])
        self.done +=1

    def bust(self, Player):
        self.players[Player].state = "busted"
        self.showCards(Player, config["colours"]["dark gray"])
        self.done +=1

    def hit(self, Player):
        if (self.players[Player].hand.total < 21):
            self.players[Player].hand.addCard(self.shoe.shoe[0])
            cardplace = self.players[Player].hand.numCards
            if  self.players[Player].hand.total > 21:
                self.bust(Player)
            elif self.players[Player].hand.total == 21:
                self.stand(Player)
            else:
                self.showCards(Player, config["colours"]["gray"])
            self.shoe.shoe.pop(0)

    def compmove(self, Player):

        print(Player)

    def dealerturn(self):
        self.showDealercards(True)
        if self.wait(800):
            if self.dealer.hand.total > 16:
                self.roundend()
            else:
                self.dealer.hand.addCard(self.shoe.shoe[0])
                self.shoe.shoe.pop(0)
                if self.wait(800):
                    self.showDealercards(True)

    def wait(self, time):
        now = pygame.time.get_ticks()
        if now - self.last >= time:
            self.last = now
            return True
        else:
            return False

    def roundend(self):
        for i in self.players:
            if i.hand.total == 21 and i.hand.numCards==2:
                i.money += int(config["setup"]["buy in"]*(3/2))
            elif i.hand.total > self.dealer.hand.total and i.hand.total <= 21:
                i.money += config["setup"]["buy in"]*2
            elif i.hand.total == self.dealer.hand.total:
                i.money += config["setup"]["buy in"]
            i.hand = hand()
            i.state = "playing"
            i.money -= config["setup"]["buy in"]
        self.dealer.hand = hand()
        self.roundSetup()

    def showCards(self, Player,colour):
        size = 12
        currplayer = self.players[Player]
        cardstoshow= range(len(currplayer.hand.cards))
        for i in cardstoshow:
            xshift = (Player+1)/(len(self.players)+1)*config["game"]['width']+5.2*[12,6,-6,0][i % 4]*2 -6*size
            yshift = config["game"]['height']*(0.765-(int((i+1)/2))*0.134)-6*size
            card = currplayer.hand.cards[i]
            pygame.draw.polygon(self.display,colour,[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
            text = self.font.render(card.uni+card.apperance+card.uni, True,config["colours"][card.colour], colour)
            textRect = text.get_rect()
            textRect.center = (xshift+6*size, yshift+6*size)
            self.display.blit(text, textRect)
        #total
        xshift = (Player+1)/(len(self.players)+1)*config["game"]['width']-6*size
        yshift = config["game"]['height']*(0.765)-6*size
        pygame.draw.polygon(self.display,colour,[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
        text = self.font.render(str(currplayer.hand.total), True,config["colours"]["green"], colour)
        textRect = text.get_rect()
        textRect.center = (xshift+6*size, yshift+6*size)
        self.display.blit(text, textRect)

        #money
        xshift = (Player+1)/(len(self.players)+1)*config["game"]['width']-0.8*size
        yshift = config["game"]['height']*(0.9)-6*size
        pygame.draw.polygon(self.display,colour,[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
        text = self.font.render("$"+str(currplayer.money), True,config["colours"]["light green"], colour)
        textRect = text.get_rect()
        textRect.center = (xshift+6*size, yshift+6*size)
        self.display.blit(text, textRect)


    def showDealercards(self, playersdone):
        size = 12
        yshift= (config["game"]['width']/12)-6*size
        if playersdone:
            cardstoshow= range(len(self.dealer.hand.cards))
            text = self.font.render(str(self.dealer.hand.total), True,config["colours"]["green"], config["colours"]["white"])
        else:
            cardstoshow= range(1)
            text = self.font.render(str(self.dealer.hand.cards[0].value), True,config["colours"]["green"], config["colours"]["white"])
            xshift = (config["game"]['width']/2)-6*size*2.5
            pygame.draw.polygon(self.display,config["colours"]["white"],[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
        xshift = (config["game"]['width']/2)-6*size

        pygame.draw.polygon(self.display,config["colours"]["white"],[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
        textRect = text.get_rect()
        textRect.center = (xshift+6*size, yshift+6*size)
        self.display.blit(text, textRect)

        for i in cardstoshow:
            card = self.dealer.hand.cards[i]
            text = self.font.render(card.uni+card.apperance+card.uni, True,config["colours"][card.colour], config["colours"]["white"])
            xshift = (config["game"]['width']/2)-6*size+((-1)**(i))*9*size*int((i+2)/2)
            pygame.draw.polygon(self.display,config["colours"]["white"],[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
            textRect = text.get_rect()
            textRect.center = (xshift+6*size, yshift+6*size)
            self.display.blit(text, textRect)
