import pygame
from typing import Callable
from game.clickable import Clickable


class Button(Clickable):
    def __init__(self,
                 option_title: str,
                 option_method: Callable,
                 method_kwargs: dict = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.title = option_title
        self.method = option_method
        self.method_kwargs = method_kwargs if method_kwargs else {}
        self.selected = True

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        """
        If clicked - trigger mapped instance method.
        """
        self.method(**self.method_kwargs)
        return super().left_upclick(mouse_event, **kwargs)

    def update(self) -> None:
        """
        Blit image on screen, then write text on it.
        """
        super().update()
        self.draw_text(self.title)
