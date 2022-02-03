import pygame
from game.clickable import Clickable


class Tapable(Clickable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tap = False
        self.untap = False
        self.tapped = False
    
    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        if self.tapped:
            self.untap = True
        else:
            self.tap = True

        return super().left_upclick(mouse_event, **kwargs)
    
    def update(self, game) -> None: 
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