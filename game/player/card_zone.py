from typing import List
import pygame
from game.player.zone import Zone
from game.player.card_group import CardGroup


class CardZone(Zone):
    def __init__(self, **kwargs):
        self.cards: List[pygame.sprite.Sprite] = CardGroup(zone=self)
        super().__init__(**kwargs)

    def distribute_cards(self):
        """
        Change coordinates of each card in this zone to distribute them equaly.
        """
        cards_count = len(self.cards)
        space_x = self.w // (cards_count + 1)
        space_y = self.h // (cards_count + 1)
        for number, card in enumerate(self.cards):
            if self.a == 90 or self.a == 270:
                card.rect.centerx = self.x + self.w // 2
                card.rect.centery = self.y + space_y * (number + 1)
            else:
                card.rect.centerx = self.x + space_x * (number + 1)
                card.rect.centery = self.y + self.h // 2
