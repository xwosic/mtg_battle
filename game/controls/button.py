import pygame
from typing import Callable
from game.clickable import Clickable


class Button(Clickable):
    def __init__(self, instance, option_title: str, option_method: Callable, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        self.title = option_title
        self.method = option_method

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        self.method()
        return super().left_upclick(mouse_event, **kwargs)
