import pygame
import random
from game.card import Card
from game.controls.search_card_view import SearchCardView
from game.game_objects.clickable import Clickable
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
        self.face_up = False

    def right_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        return super().right_upclick(mouse_event, **kwargs)

    def search(self):
        SearchCardView(game=self.game, pile=self.pile)

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        self.search()
        return super().left_upclick(mouse_event, **kwargs)

    def put_card_on_top(self, card_view):
        self.pile.cards.append(card_view.name)
        self.get_image_from_card(card_view)
        card_view.kill()

    def get_image_from_card(self, card_view):
        self.image = card_view.image
        self.change_scale(self.WIDTH / self.image.get_width())

    def update(self) -> None:
        if self.pile.cards:
            if self.image:
                super().update()

            else:
                if self.face_up:
                    card = self.pile.get_top_card()
                    if card is not None:
                        self.get_image_from_card(card.view)


class Pile:
    def __init__(self, **kwargs):
        self.cards: List[str] = []
        self.view = PileVisualization(pile=self, **kwargs)

    def get_top_card(self) -> Card:
        """
        Get top card of Pile as Card instance.
        Returned card is detached from all group and won't be displayed.
        Card can be added to another group.
        """
        if self.cards:
            name = self.cards[-1]
            card = Card(name=name, game=self.view.game)
            card.view.kill()
            return card
        return None

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def match_card_name(self, value: str) -> List[str]:
        """
        Returns list of matching card names.
        """
        return [name for name in self.cards if value.lower() in name.lower()]

    def remove_card(self, card_name: str):
        if card_name in self.cards:
            self.cards.remove(card_name)

    def update(self):
        self.view.update()
