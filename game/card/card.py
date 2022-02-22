import pygame
from game.game_objects import Tapable
from pathlib import Path
from game.controls.dropdown_view import DropdownView
from game.controls.counter import DiceCounter


class Card:
    pass


tmp_scale = 1.75


class CardVisualization(Tapable):
    WIDTH = int(63 * tmp_scale)
    HEIGHT = int(88 * tmp_scale)
    DEFAULT_PATH = 'cards'

    def __init__(self,
                 name: str,
                 card: Card = None,
                 default_path: str = None,
                 scale: float = None,
                 **kwargs):
        self.name = name
        self.card = card if card else None
        self.DEFAULT_PATH = default_path if default_path else self.DEFAULT_PATH

        image = self.find_image(name)
        unified_scale = self.unify_scale(image, **kwargs)
        scale = scale * unified_scale if scale else unified_scale
        super().__init__(image=image, scale=scale, **kwargs)
        self.game.sprite_group.add(self)
        self.right_click_options['add_counter'] = {'instance': self, 'kwargs': {'value': 1}}

    def right_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        DropdownView(game=self.game, options=self.right_click_options)

    def find_image(self, name: str):
        """
        Loades name.jpg from the directory.
        """
        path_to_card = Path.joinpath(Path(self.DEFAULT_PATH), f'{name}.jpg')
        image = pygame.image.load(path_to_card)
        return image

    def unify_scale(self, image: pygame.Surface, **kwargs):
        """
        Image size is compared to the pattern and fix scale is computed.
        """
        if 'game' in kwargs:
            game_screen_h = kwargs['game'].screen.height
            one_card_h = game_screen_h // 6
            actual_height = image.get_height()
            ratio = actual_height / one_card_h
            return 1 / ratio

        actual_width = image.get_width()
        ratio = actual_width / self.WIDTH
        scale_to_unify = 1 / ratio
        return scale_to_unify

    def add_counter(self, value):
        DiceCounter.create_card_counter(card=self, init_value=value)

    def __repr__(self):
        return f'CardVisualization(name={self.card.name})'


class Card:
    def __init__(self,
                 name: str,
                 **kwargs):
        self.name = name
        self.view = CardVisualization(card=self, name=name, **kwargs)

    def __repr__(self):
        return f'Card(name={self.name})'
