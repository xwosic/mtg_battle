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
                 c = (0, 0, 0),
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
    
    def calculate_rotation(self, x, y, angle, scale):
        angle_radians = angle * pi / 180
        delta_x = x * cos(angle_radians) - y * sin(angle_radians)
        delta_y = x * sin(angle_radians) + y * cos(angle_radians)
        return delta_x * scale, delta_y * scale

    def update(self):
        pygame.draw.polygon(self.game.screen.screen,
                            self.color,
                            [self.tl, self.tr, self.br, self.bl, self.tl],
                            width=1)
