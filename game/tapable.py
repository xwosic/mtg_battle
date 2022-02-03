import pygame
from game.dragable import Dragable


class Tapable(Dragable):
    """
    Class inheriting after Tapable has tap and untap functionality.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tap = False
        self.untap = False
        self.tapped = False
        self.tap_start_position = (0,0)
        self.tap_end_position = (0,0)

    def left_click(self, mouse_event: pygame.event.Event, **kwargs):
        """
        When MLB is pressed current position is checked.
        """
        self.tap_start_position = mouse_event.pos
        return super().left_click(mouse_event, **kwargs)
    
    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        """
        When MLB is method checks if object moved. If so, no tap/untap will be performed.
        """
        self.tap_end_position = mouse_event.pos
        delta_x = self.tap_end_position[0] - self.tap_start_position[0]
        delta_y = self.tap_end_position[1] - self.tap_start_position[1]

        # when drag'n'drop is performed flags have to be reset
        if delta_x and delta_y:
            self.tap = False
            self.untap = False
        else:
            if self.tapped:
                self.untap = True
            else:
                self.tap = True
        return super().left_upclick(mouse_event, **kwargs)
    
    def update(self, game) -> None:
        """
        On update the tap or untap is performed only once.
        """
        if self.tap:
            self.tap = False
            if not self.tapped:
                self.tapped = True
                position = self.rect.center
                self.image = pygame.transform.rotate(self.image, -90)
                self.rect = self.image.get_rect()
                self.rect.center = position
            
        if self.untap:
            self.untap = False
            if self.tapped:
                self.tapped = False
                position = self.rect.center
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect = self.image.get_rect()
                self.rect.center = position

        return super().update(game)
