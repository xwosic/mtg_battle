import pygame
from game.clickable import Clickable


class ClickableDropable(Clickable):
    """
    Class inheriting after ClickableDropable has click and drop into functionality.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.tap_start_position = (0,0)
        # self.tap_end_position = (0,0)
        self.left_clicked = False

    def left_click(self, mouse_event: pygame.event.Event, **kwargs):
        """
        When MLB is pressed current position is checked.
        """
        self.left_clicked = True
        # self.tap_start_position = mouse_event.pos
        return super().left_click(mouse_event, **kwargs)
    
    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        """
        When MLB is method checks if object moved. If so, no tap/untap will be performed.
        """
        # self.tap_end_position = mouse_event.pos
        # delta_x = self.tap_end_position[0] - self.tap_start_position[0]
        # delta_y = self.tap_end_position[1] - self.tap_start_position[1]

        if self.left_clicked:
            # normal click
            self.left_upclicked_trigger(mouse_event=mouse_event, **kwargs)
        else:
            # dragged over and drop
            self.drop_trigger(mouse_event=mouse_event, **kwargs)
  
        self.left_clicked = False
        return super().left_upclick(mouse_event, **kwargs)
    
    def left_upclicked_trigger(self, **kwargs):
        pass

    def drop_trigger(self, **kwargs):
        pass
