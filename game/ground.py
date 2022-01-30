import pygame
from game.animation_less import AnimationLess


class Ground(AnimationLess):
    def __init__(self, x, y, width, heigth, **kwargs):
        super().__init__(width, heigth, **kwargs)
        self.rect.x = x
        self.rect.y = y


    def add_gravity(self, game):
        pass

    def collide_with_tiles(self, game):
        pass

    def get_hit(self, demage, game):
        pass

    def prevent_collisions(self, game):
        pass