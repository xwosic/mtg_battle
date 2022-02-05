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
        
        # todo - create good rectangle!!!
    
    def calculate_rotation(self, x, y, angle, scale):
        angle_radians = angle * pi / 180
        delta_x = x * cos(angle_radians) - y * sin(angle_radians)
        delta_y = x * sin(angle_radians) + y * cos(angle_radians)
        return delta_x * scale, delta_y * scale
    
    def is_rotated(self):
        return self.a == 90 or self.a == 270
    
    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        x = pos[0]
        y = pos[1]
        print(self.tl, self.br, pos)
        if self.tl[0] <= x <= self.tr[0]:
            if self.tl[1] >= y >= self.bl[1]:
                print('tru')
                return True
        print('fol')
        return False
    
    def add_card(self, card):
        pass

    def left_upclick(self, mouse_event: pygame.event.Event, dragged, **kwargs):
        """
        Object is dropped when mouse's left button is reliesed.
        """
        pass

    def update(self):
        pygame.draw.polygon(self.game.screen.screen,
                            self.color,
                            [self.tl, self.tr, self.br, self.bl, self.tl],
                            width=1)
