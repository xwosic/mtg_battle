from game.game_object import GameObject
from pathlib import Path
from mtg_deck_reader import read_deck


class DeckVisualization(GameObject):
    WIDTH = 63 * 2
    HEIGHT = 88 * 2
    def __init__(self, name: str, **kwargs):
        super().__init__(width=self.WIDTH, height=self.HEIGHT, **kwargs)
        self.name = name


class Deck:
    DEFAULT_PATH = 'decks'
    def __init__(self,
                 name: str,
                 default_path: str = None,
                 **kwargs):
        self.name = name           
        self.view = DeckVisualization(name=name, **kwargs)
        self.DEFAULT_PATH = default_path if default_path else self.DEFAULT_PATH
        deck_setup = self.get_cards_from_txt(name)
        self.cards = self.create_deck(deck_setup)
    
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