import pygame
from pathlib import Path
from mtg_deck_reader import read_deck
from game.card import Card
from game.pile import Pile, PileVisualization
import random


class Player:
    pass


class DeckVisualization(PileVisualization):

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        self.pile.draw()
        return super().left_upclick(mouse_event, **kwargs)


class Deck(Pile):
    DEFAULT_PATH = 'decks'

    def __init__(self,
                 player: Player,
                 name: str,
                 default_path: str = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.view = DeckVisualization(pile=self, **kwargs)
        self.name = name
        self.player = player
        self.DEFAULT_PATH = default_path if default_path else self.DEFAULT_PATH
        deck_setup = self.get_cards_from_txt(name)
        self.cards = self.create_deck(deck_setup)
        random.shuffle(self.cards)

    def get_cards_from_txt(self, name: str) -> dict:
        """
        Get dict of mainboard and sideboard.
        """
        path_to_deck = Path.joinpath(Path(self.DEFAULT_PATH), f'{name}.txt')
        return read_deck(path_to_deck)

    def create_deck(self, deck_setup: dict):
        """
        Adds cards to deck in number as in deck setup dict.
        """
        cards = []
        for name, quantity in deck_setup['mainboard'].items():
            for _ in range(quantity):
                cards.append(name)

        return cards

    def draw(self):
        """
        Put top card of deck and place it in hand.
        """
        if self.cards:
            card_name = self.cards.pop()
            self.player.hand.add_card(Card(game=self.view.game,
                                           groups=[self.player.game.sprite_group],
                                           name=card_name))
