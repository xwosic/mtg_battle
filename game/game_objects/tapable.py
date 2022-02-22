import pygame
from .attachable import Attachable


class Tapable(Attachable):
    """
    Class inheriting after Tapable has tap and untap functionality.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tap = False
        self.untap = False
        self.tapped = False

    def left_upclick(self, **kwargs):
        """
        Clicking on objects toggles it's state (tap/untap).
        """
        if self.tapped:
            self.untap = True
            self.tap = False

        else:
            self.untap = False
            self.tap = True

    def update(self) -> None:
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

        return super().update()
