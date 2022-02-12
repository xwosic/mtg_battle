import pygame
from typing import Callable
from game.game_objects.clickable import Clickable


class Button(Clickable):
    def __init__(self,
                 option_title: str,
                 option_method: Callable,
                 parent=None,
                 method_kwargs: dict = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.title = option_title
        self.method = option_method
        self.method_kwargs = method_kwargs if method_kwargs else {}
        self.selected = True
        self.parent = parent

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        """
        If clicked - trigger mapped instance method.
        """
        self.method(**self.method_kwargs)
        if self.parent:
            self.parent.kill()
        self.kill()

    def update(self) -> None:
        """
        Blit image on screen, then write text on it.
        """
        super().update()
        self.draw_text(self.title)
