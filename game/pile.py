import pygame
from game.clickable import Clickable
import random
from typing import List


class Player:
    pass


class Pile:
    pass


class PileVisualization(Clickable):
    WIDTH = 63 * 1
    HEIGHT = 88 * 1

    def __init__(self, pile: Pile, **kwargs):
        super().__init__(width=self.WIDTH, height=self.HEIGHT, **kwargs)
        self.pile = pile

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        return super().left_upclick(mouse_event, **kwargs)

    def put_card_on_top(self, card_view):
        self.pile.cards.append(card_view.name)
        card_view.kill()


class Pile:
    def __init__(self, **kwargs):
        self.cards: List[str] = []
        self.view = PileVisualization(pile=self, **kwargs)

    def shuffle(self):
        if self.cards:
            random.shuffle(self.cards)
