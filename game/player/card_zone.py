import pygame
from game.player.zone import Zone
from game.player.card_group import CardGroup


class CardZone(Zone):
    def __init__(self, **kwargs):
        self.cards = CardGroup(zone=self)
        super().__init__(**kwargs)

    def distribute_cards(self):
        """
        Change coordinates of each card in this zone to distribute them equaly.
        """
        cards_count = len(self.cards)
        space_x = self.w // (cards_count + 1)
        space_y = self.h // (cards_count + 1)
        for number, card in enumerate(self.cards):
            card.rect.x = self.x + space_x * (number + 1)
            card.rect.y = self.y + space_y * (number + 1)
