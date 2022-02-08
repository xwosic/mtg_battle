import pygame
from game.game_object import GameObject


class Clickable(GameObject):
    """
    Class inheriting after Clickable will be triggered by Mouse class
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def left_click(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def right_click(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def right_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def update(self) -> None:
        return super().update()
        