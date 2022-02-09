from typing import Union, Iterable, Sequence
import pygame
from pygame.sprite import Sprite, AbstractGroup


class CardZone:
    pass


class CardGroup(pygame.sprite.Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]], zone: CardZone) -> None:
        """
        This is small wrapper for sprine group. It handles pointer to it's Zone.
        """
        self.zone = zone
        super().__init__(*sprites)

    def add(self, *sprites: Union[Sprite, AbstractGroup, Iterable[Union[Sprite, AbstractGroup]]]) -> None:
        """
        When card is added to group cards are redistributed within it.
        """
        super().add(*sprites)
        if len(self.sprites()) > 0:
            self.zone.distribute_cards()

    def remove(self, *sprites: Sprite) -> None:
        """
        When card is removed from group, zone recalculates positions of remaining cards.
        """
        super().remove(*sprites)
        if len(self.sprites()) > 0:
            self.zone.distribute_cards()
