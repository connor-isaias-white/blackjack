import pygame

from src.game import Game
from src.config import config

def main():
    display = pygame.display.set_mode((
        config['game']['width'],
        config['game']['height']
    ))
    pygame.display.set_caption(config['game']['caption'])

    game = Game(display)
    game.loop()

if __name__ == '__main__':
    main()
