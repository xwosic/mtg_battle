import pygame
from game.game_object import GameObject


class Clickable(GameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drag = False
        self.mouse_offset = (0,0)
    
    def left_click(self, mouse_event: pygame.event.Event, **kwargs):
        self.drag = True
        self.mouse_offset = (mouse_event.pos[0] - self.rect.x, mouse_event.pos[1] - self.rect.y)

    def right_click(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        self.drag = False


    def right_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        pass

    def update(self, game) -> None:
        if self.drag:
            self.rect.x = pygame.mouse.get_pos()[0] - self.mouse_offset[0]
            self.rect.y = pygame.mouse.get_pos()[1] - self.mouse_offset[1]
        
        return super().update(game)
        