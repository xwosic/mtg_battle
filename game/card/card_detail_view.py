import pygame
from game.game_objects import GameObject
from pathlib import Path


tmp_scale = 3.0


class CardDetailView(GameObject):
    WIDTH = int(63 * tmp_scale)
    HEIGHT = int(88 * tmp_scale)
    DEFAULT_PATH = 'cards'

    def __init__(self,
                 name: str,
                 scale: float = None,
                 **kwargs):
        self.name = name
        image = self.find_image(name)
        unified_scale = self.unify_scale(image, **kwargs)
        scale = scale * unified_scale if scale else unified_scale
        super().__init__(image=image, scale=scale, **kwargs)
        self.game.sprite_group.add(self)

        if kwargs.get('x') is not None:
            print(kwargs.get('x'))
            self.rect.x = self.rect.x + self.rect.width // 2

        if kwargs.get('y') is not None:
            print(kwargs.get('y'))
            self.rect.y = self.rect.y + self.rect.height // 2

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
        actual_width = image.get_width()
        ratio = actual_width / self.WIDTH
        scale_to_unify = 1 / ratio
        return scale_to_unify
