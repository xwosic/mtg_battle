from typing import Tuple
import pygame
from math import cos, sin, pi


class Game:
    pass


class Zone:
    def __init__(self,
                 game: Game,
                 x=0,
                 y=0,
                 w=100,
                 h=10,
                 a=0.0,
                 scale=1.0,
                 c=(0, 0, 0),
                 **kwargs):
        self.game = game

        self.a = a
        self.scale = scale
        self.x, self.y = x, y
        self.w, self.h = self.calculate_rotation(w,  h, self.a, self.scale)
        self.color = c

        self.tl = (self.x, self.y)
        self.bl = (self.x, self.y + self.h)
        self.tr = (self.x + self.w, self.y)
        self.br = (self.x + self.w, self.y + self.h)
        self.rect = pygame.rect.Rect((self.find_top_left_corner()), (abs(self.w), abs(self.h)))

    def calculate_rotation(self, x, y, angle, scale):
        angle_radians = angle * pi / 180
        delta_x = x * cos(angle_radians) - y * sin(angle_radians)
        delta_y = x * sin(angle_radians) + y * cos(angle_radians)
        return delta_x * scale, delta_y * scale

    def is_rotated(self):
        return self.a == 90 or self.a == 270

    def find_top_left_corner(self):
        corners = [self.tl, self.tr, self.bl, self.br]
        min_x = None
        min_y = None
        for corner in corners:
            if min_x is None:
                min_x = corner[0]
            elif min_x >= corner[0]:
                min_x = corner[0]
            if min_y is None:
                min_y = corner[1]
            elif min_y >= corner[1]:
                min_y = corner[1]

        return min_x, min_y

    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    def add_card(self, card):
        pass

    def left_upclick(self, mouse_event: pygame.event.Event, dragged, **kwargs):
        """
        Object is dropped when mouse's left button is reliesed.
        """
        pass

    def update(self):
        pygame.draw.rect(self.game.screen.screen,
                         self.color,
                         self.rect,
                         width=1)
