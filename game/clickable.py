import pygame
from game.game_object import GameObject
from typing import Tuple


class Clickable(GameObject):
    """
    Class inheriting after Clickable will be triggered by Mouse class
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.right_click_options = []

    def left_click(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def right_click(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def right_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    def update(self) -> None:
        return super().update()

    @property
    def options(self):
        return {'instance': self, 'options': self.right_click_options}
