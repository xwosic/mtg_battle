import pygame
from game.clickable import Clickable


class Dragable(Clickable):
    """
    Class inheriting after Dragable has drag and drop functionality.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drag = False
        self.mouse_offset = (0,0)
    
    def left_click(self, mouse_event: pygame.event.Event, **kwargs):
        """
        Dragging starts after mouse's left button is clicked.
        """
        self.drag = True
        self.mouse_offset = (mouse_event.pos[0] - self.rect.x, mouse_event.pos[1] - self.rect.y)
        return super().left_click(mouse_event, **kwargs)

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        """
        Object is dropped when mouse's left button is reliesed.
        """
        self.drag = False
        return super().left_upclick(mouse_event, **kwargs)

    def update(self, game) -> None:
        """
        If mouse's left button is pressed and mouse is moving, object will follow.
        """
        if self.drag:
            self.rect.x = pygame.mouse.get_pos()[0] - self.mouse_offset[0]
            self.rect.y = pygame.mouse.get_pos()[1] - self.mouse_offset[1]
        
        return super().update(game)