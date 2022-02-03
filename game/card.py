import pygame
from game.tapable import Tapable
from typing import List
from pathlib import Path


class Card:
    pass


class CardVisualization(Tapable):
    WIDTH = 63 * 4
    HEIGHT = 88 * 4
    DEFAULT_PATH = 'cards'
    def __init__(self, 
                 name: str,
                 card: Card = None, 
                 default_path: str = None,
                 **kwargs):
        self.name = name
        self.card = card if card else None
        self.DEFAULT_PATH = default_path if default_path else self.DEFAULT_PATH

        image = self.find_image(name)
        scale = self.unify_scale(image)
        super().__init__(image=image, scale=scale, **kwargs)

        # card is held in bottom left corner - easier pivot
        self.rect.center = self.rect.bottomleft

    def find_image(self, name: str):
        """
        Loades name.jpg from the directory.
        """
        path_to_card = Path.joinpath(Path(self.DEFAULT_PATH), f'{name}.jpg')
        image = pygame.image.load(path_to_card)
        return image
    
    def unify_scale(self, image: pygame.Surface):
        """
        Image size is compared to the pattern and fix scale is computed.
        """
        actual_width = image.get_width()
        ratio = actual_width / self.WIDTH
        scale_to_unify = 1 / ratio
        return scale_to_unify


class Card:
    def __init__(self,
                 name: str,
                 **kwargs):
        self.name = name
        self.tapped = False
        self.view = CardVisualization(card=self, name=name, **kwargs)
