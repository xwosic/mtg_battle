import pygame
from game.sth import Sth


class AnimationLess(Sth):
    def update_animation(self, states):
        # this class and it's children has no animation
        pass

    def is_event_triggered(self, game):
        pass
