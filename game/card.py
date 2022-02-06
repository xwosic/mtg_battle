import pygame
from game.tapable import Tapable
from pathlib import Path


class Card:
    pass

tmp_scale = 1.25

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
        unified_scale = self.unify_scale(image)
        scale = scale * unified_scale if scale else unified_scale
        super().__init__(image=image, scale=scale, **kwargs)
        self.game.sprite_group.add(self)

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
        self.view = CardVisualization(card=self, name=name, **kwargs)
