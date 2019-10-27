import pygame
from src.config import config

class Game:
    def __init__(self, display):
        self.display = display
        self.running = True

    def loop(self):
        clock = pygame.time.Clock()
        while self.running:
            self.events()
            pygame.display.update()
            clock.tick(config['game']['fps'])

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                exit()
