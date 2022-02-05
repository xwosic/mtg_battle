from typing import List
import pygame
from game.player.zone import Zone
from game.player.card_group import CardGroup
from game.card import Card


class CardZone(Zone):
    def __init__(self, **kwargs):
        self.cards = pygame.sprite.Group()
        super().__init__(**kwargs)
    
    def add_card(self, card: Card):
        self.cards.add(card.view)
        self.game.sprite_group.add(card.view)
        if len(self.cards) > 0:
            self.distribute_cards()
    
    def remove_card(self, card: Card):
        if card.view in self.cards:
            self.cards.remove(card.view)
            self.game.sprite_group.remove(card.view)
            self.distribute_cards()
        return card.name

    def distribute_cards(self):
        """
        Change coordinates of each card in this zone to distribute them equaly.
        """
        cards_count = len(self.cards)
        space_x = self.w // (cards_count + 1)
        space_y = self.h // (cards_count + 1)
        for number, card in enumerate(self.cards):
            if self.is_rotated():
                card.rect.centerx = self.x + self.w // 2
                card.rect.centery = self.y + space_y * (number + 1)
            else:
                card.rect.centerx = self.x + space_x * (number + 1)
                card.rect.centery = self.y + self.h // 2
