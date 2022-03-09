import pygame
import random
from game.card import Card
from game.controls.dropdown_view import DropdownView
from game.controls.scry_view import ScryView
from game.controls.surveil_view import SurveilView
from game.controls.search_card_view import SearchCardView
from game.controls.token_view import TokenView
from game.piles.pile import Pile, PileVisualization
from mtg_api.asyncho import download_cards
from mtg_api.sync import check_which_card_to_download
from mtg_deck_reader import DeckReader
from pathlib import Path


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
    deck_reader = DeckReader(deck_path)
    deck = deck_reader.read_deck()
    # commander
    commander = list(deck['commander'].keys())
    cards_to_download = check_which_card_to_download(commander, path_to_cards)
    download_cards(cards_to_download, path_to_cards)
    # mainboard
    mainboard = list(deck['mainboard'].keys())
    cards_to_download = check_which_card_to_download(mainboard, path_to_cards)
    download_cards(cards_to_download, path_to_cards)
    # sideboard
    sideboard = list(deck['sideboard'].keys())
    cards_to_download = check_which_card_to_download(sideboard, path_to_cards)
    download_cards(cards_to_download, path_to_cards)
    # tokens
    tokens = list(deck['tokens'].keys())
    tokens_to_download = check_which_card_to_download(tokens, path_to_cards)
    download_cards(tokens_to_download, path_to_cards, token_queries=deck['tokens'])


class Player:
    pass


class DeckVisualization(PileVisualization):
    def __init__(self, pile: Pile, **kwargs):
        super().__init__(pile, **kwargs)
        self.face_up = False
        self.right_click_options = {
                     'search': {'instance': self, 'kwargs': {}},
                     'shuffle': {'instance': self.pile, 'kwargs': {}},
                     'scry': {'instance': self, 'kwargs': {'number_of_cards': 1}},
                     'surveil': {'instance': self, 'kwargs': {'number_of_cards': 1}},
                     'mill': {'instance': self.pile, 'kwargs': {'number_of_cards': 1}},
                     'add_token': {'instance': self, 'kwargs': {}},
                     }

    def right_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        DropdownView(game=self.game, options=self.right_click_options)

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        self.pile.draw()

    def search(self):
        SearchCardView(game=self.game, pile=self.pile, shuffle_after_search=True)

    def scry(self, number_of_cards=1):
        ScryView(game=self.game, player=self.pile.player, pile=self.pile, number_of_cards=number_of_cards)

    def surveil(self, number_of_cards=1):
        SurveilView(game=self.game, player=self.pile.player, pile=self.pile, number_of_cards=number_of_cards)

    def add_token(self):
        TokenView(game=self.game, pile=self.pile)


class Deck(Pile):
    DEFAULT_PATH = 'decks'

    def __init__(self,
                 name: str,
                 default_path: str = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.view = DeckVisualization(pile=self, **kwargs)
        self.name = name
        self.DEFAULT_PATH = default_path if default_path else self.DEFAULT_PATH
        deck_setup = self.get_cards_from_txt(name)
        self.commander, self.cards, self.tokens = self.create_deck(deck_setup)
        random.shuffle(self.cards)
        if self.commander:
            self.cards.append(self.commander)

    def get_cards_from_txt(self, name: str) -> dict:
        """
        Get dict of mainboard and sideboard.
        """
        path_to_deck = Path.joinpath(Path(self.DEFAULT_PATH), f'{name}.txt')
        return DeckReader(path_to_deck).read_deck()

    def create_deck(self, deck_setup: dict):
        """
        Adds cards to deck in number as in deck setup dict.
        """
        commander = [c for c in deck_setup['commander'].keys()]
        if commander:
            commander = commander[0]

        cards = []
        for name, quantity in deck_setup['mainboard'].items():
            for _ in range(quantity):
                cards.append(name)

        tokens = []
        for name in deck_setup['tokens'].keys():
            tokens.append(name)

        return commander, cards, tokens

    def scry(self, number_of_cards: str):
        """
        Returns x top cards.
        """
        try:
            number_of_cards = int(number_of_cards)
        except ValueError:
            return []

        if number_of_cards <= len(self.cards):
            if self.cards:
                scry_cards = []
                for _ in range(number_of_cards):
                    scry_cards.append(self.cards.pop())
                return scry_cards

    def draw(self):
        """
        Put top card of deck and place it in hand.
        """
        if self.cards:
            card_name = self.cards.pop()
            self.view.image = None
            card = Card(game=self.view.game, name=card_name)
            card.view.rect.center = self.view.rect.center
            self.player.hand.add_card(card)
        self.view.selected = False

    def mill(self, number_of_cards: str):
        try:
            number_of_cards = int(number_of_cards)
        except ValueError:
            return

        for _ in range(number_of_cards):
            if self.cards:
                card_name = self.cards.pop()
                self.view.image = None
                card = Card(game=self.view.game, name=card_name)
                self.player.graveyard.view.put_card_on_top(card.view)
