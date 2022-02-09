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
        self.get_image_from_card(card_view)
        card_view.kill()

    def get_image_from_card(self, card_view):
        self.image = card_view.image
        self.change_scale(self.WIDTH / self.image.get_width())

    def update(self) -> None:
        if self.image:
            super().update()


class Pile:
    def __init__(self, **kwargs):
        self.cards: List[str] = []
        self.view = PileVisualization(pile=self, **kwargs)

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def update(self):
        self.view.update()
