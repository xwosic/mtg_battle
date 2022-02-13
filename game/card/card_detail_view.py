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
    def __init__(self, mouse, mouse_quarter, **kwargs):
        self.mouse = mouse
        kwargs['game'] = mouse.game if kwargs.get('game') is None else kwargs['game']

        super().__init__(**kwargs)
        self.place_in_quarter(mouse_quarter)

    def place_in_quarter(self, mouse_quarter):
        """
        Place card detail in opposite quarter to actual mouse position.
        """
        if mouse_quarter == 'br':
            x, y = 0, 0
        elif mouse_quarter == 'bl':
            x, y = self.game.screen.width - self.rect.width, 0
        elif mouse_quarter == 'tl':
            x, y = self.game.screen.width - self.rect.width, self.game.screen.height - self.rect.height
        elif mouse_quarter == 'tr':
            x, y = 0, self.game.screen.height - self.rect.height

        self.rect.x = x
        self.rect.y = y

    def update(self) -> None:
        if self.mouse is None:
            self.kill()

        return super().update()
