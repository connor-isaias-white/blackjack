import pygame
from src.config import config
from src.deck import deck
from src.player import player
from random import randint
from src.hand import hand
from src.basic import basic
from time import sleep
from random import getrandbits

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
        self.realplayers = False

    def loop(self):
        self.shoe = deck(20)
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
                    elif event.key == pygame.K_d:
                        self.doubleDown(self.turn % len(self.players))
                        self.turn +=1

    def setupPlayers(self):
        for i in range(config["setup"]["players"]):
            if i == 0 and not config["setup"]["comps only"]:
                Player = player(i, False, False)
                self.realplayers = True
            else:
                Player = player(i, False, True)
            self.players.append(Player)

    def roundSetup(self):
        self.display.fill(config["colours"]["black"])
        self.turn = 0
        self.done = 0
        if len(self.shoe.shoe) < self.shoe.cutCard:
            self.shoe = deck(20)
            self.shoe.shuffle()
        for i in range(len(self.players)*2):
            if self.players[i % len(self.players)].state != "out":
                self.hit(i % len(self.players))
            else:
                self.done += 0.5
        if self.done == config["setup"]["players"]:
            self.players = []
            self.setupPlayers()

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

    def doubleDown(self, Player):
        self.players[Player].state = "doubled"
        self.players[Player].money -= config["setup"]["buy in"]
        self.hit(Player)
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
        if self.players[Player].strat == "basic":
            if self.players[Player].hand.numaces > 0:
                ace = "ace"
            else:
                ace = "noAce"
            if basic[ace][str(self.players[Player].hand.total)][self.dealer.hand.cards[0].value] == 'h':
                self.hit(Player)
            else:
                self.stand(Player)
        elif self.players[Player].strat == "standat17":
            if self.players[Player].hand.total <17:
                self.hit(Player)
            else:
                self.stand(Player)
        elif self.players[Player].strat == "drunk":
            move = getrandbits(1)
            if move:
                self.hit(Player)
            else:
                self.stand(Player)



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
        if self.realplayers:
            now = pygame.time.get_ticks()
            if now - self.last >= time:
                self.last = now
                return True
            else:
                return False
        else:
            return True

    def roundend(self):
        for i in self.players:
            if i.state == "doubled":
                multiplyer = 2
            else:
                multiplyer = 1

            if i.hand.total == 21 and i.hand.numCards==2 and not (self.dealer.hand.total == 21 and self.dealer.hand.numCards ==2):
                i.money += int(config["setup"]["buy in"]*(3/2))
            elif i.hand.total > self.dealer.hand.total and i.hand.total <= 21:
                i.money += config["setup"]["buy in"]*2*multiplyer
            elif i.hand.total == self.dealer.hand.total:
                i.money += config["setup"]["buy in"]*multiplyer
            i.hand = hand()

            if i.money > 0:
                i.state = "playing"
                i.money -= config["setup"]["buy in"]
            else:
                i.state = "out"
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
