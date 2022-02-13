import pygame
from game.game_objects import GameObject
from pathlib import Path


tmp_scale = 4.0


class CardView(GameObject):
    WIDTH = int(63 * tmp_scale)
    HEIGHT = int(88 * tmp_scale)
    DEFAULT_PATH = 'cards'

    def __init__(self,
                 name: str,
                 scale: float = None,
                 **kwargs):
        self.name = name
        image = self.find_image(name)
        super().__init__(image=image, **kwargs)
        self.game.sprite_group.add(self)

        if kwargs.get('x') is not None:
            self.rect.x = self.rect.x + self.rect.width // 2

        if kwargs.get('y') is not None:
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


class CardDetailView(CardView):
    def __init__(self, mouse, **kwargs):
        if kwargs.get('game') is None:
            kwargs['game'] = mouse.game

        super().__init__(x=0, y=0, **kwargs)
        self.mouse = mouse

    def update(self) -> None:
        if self.mouse is None:
            self.kill()

        return super().update()
