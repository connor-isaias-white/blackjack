import pygame
from src.config import config
from src.deck import deck
from random import randint

class Game:
    def __init__(self, display):
        pygame.init()
        self.display = display
        self.running = True
        self.font = pygame.font.Font('assets/FiraCode.ttf', 42)

    def loop(self):
        shoe = deck(2)
        shoe.shuffle()
        clock = pygame.time.Clock()
        self.showcard(shoe.shoe[0])

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
                    self.showcard(shoe.shoe[randint(0, shoe.numDecks*52-1)])

    def showcard(self, card):
        size = 12
        xshift = config["game"]["width"]/2
        yshift = config["game"]["height"]/2
        pygame.draw.polygon(self.display,config["colours"]["white"],[(0.803847577*size+xshift,3*size+yshift),(0.803847577*size+xshift,9*size+yshift),(6*size+xshift,12*size+yshift),(11.196152423*size+xshift, 9*size+yshift),(11.196152423*size+xshift,3*size+yshift),(6*size+xshift,0*size+yshift)])
        text = self.font.render(card.uni+card.apperance+card.uni, True,config["colours"][card.colour], config["colours"]["white"])
        textRect = text.get_rect()
        textRect.center = (xshift+6*size, yshift+6*size)
        self.display.blit(text, textRect)
