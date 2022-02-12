import pygame
from pathlib import Path
from mtg_deck_reader import read_deck
from game.card import Card
from game.controls.dropdown_view import DropdownView
from game.piles.pile import Pile, PileVisualization
from mtg_api.sync import check_which_card_to_download
from mtg_api.asyncho import download_cards
import random


def download_all_decks_images():
    deck_names = get_deck_filenames()
    for deck_name in deck_names:
        get_deck_images(deck_name)


def get_deck_filenames(path='decks'):
    path_to_decks = Path(path)
    deck_filenames = []
    for filename in path_to_decks.iterdir():
        if filename.is_file():
            deck_filenames.append(filename)

    return deck_filenames


def get_deck_images(deck_path: str):
    path_to_cards = Path('cards')
    deck = read_deck(deck_path)
    deck = list(deck['mainboard'].keys())
    cards_to_download = check_which_card_to_download(deck, path_to_cards)
    download_cards(cards_to_download, path_to_cards)


class Player:
    pass


class DeckVisualization(PileVisualization):
    def __init__(self, pile: Pile, **kwargs):
        super().__init__(pile, **kwargs)
        self.face_up = False
        self.right_click_options = {
                     'draw': {'instance': self.pile, 'kwargs': {}},
                     'search': {'instance': self, 'kwargs': {}}
                     }

    def right_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        DropdownView(game=self.game, options=self.right_click_options)

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        self.pile.draw()


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
            self.view.image = None
            card = Card(game=self.view.game,
                        groups=[self.player.game.sprite_group],
                        name=card_name)
            card.view.rect.center = self.view.rect.center
            self.player.hand.add_card(card)
