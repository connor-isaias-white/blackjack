import pygame

from src.game import Game
from src.config import config

def main():
    print("Controls: h to hit, s to stand, d to double down")
    try:
        dealerstand = int(input("When should the dealer stand? e.g 17: "))
    except Exception:
        dealerstand = 17
    strat = input('what strategy should the computers use? pick out of: rand, basic, standat17, any: ').lower()
    if strat not in ["rand", "basic", "standat17"]:
        strat = "any"
    display = pygame.display.set_mode((
        config['game']['width'],
        config['game']['height']
    ))
    pygame.display.set_caption(config['game']['caption'])

    game = Game(display, strat, dealerstand)
    game.loop()

if __name__ == '__main__':
    main()
