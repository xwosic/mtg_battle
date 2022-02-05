import pygame
from game.player.zone import Zone
from math import cos, sin, pi

class Player:
    pass


class Hand(Zone):
    def __init__(self, player: Player, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.cards = pygame.sprite.Group()
        print(self.x, self.y)
    
    def distribute(self):
        """
        Change coordinates of each card in this zone to distribute them equaly.
        """
        cards_count = len(self.cards)
        space_x = self.w // (cards_count + 1)
        space_y = self.h // (cards_count + 1)
        for number, card in enumerate(self.cards):
            card.rect.x = self.rect.x + space_x * (number + 1)
            card.rect.y = self.rect.y + space_y * (number + 1)
