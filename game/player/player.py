from math import cos, sin, pi
import pygame
from game.deck import Deck
from .hand import Hand


class Game:
    pass


class Player:
    """
    Player class has to provide scalable and easy to rotate map of containers on screen.
    
    There will be couple of sprite groups to handle this:
        Hand
        Battlefield
            Arena
            Lands
        Graveyard
        Exile
        View (many cards with search)
        Detail (one card when hover over)
        Air (during drag ang drop)
    
    Player will get rotation angle and rectangle to "fit in", also each player will have his/her own deck.
    """
    def __init__(self,
                 game: Game,
                 deck: Deck,
                 x: int = 0,
                 y: int = 0,
                 w: int = 100,
                 h: int = 100,
                 a: float = 0.0,
                 c = None,
                 scale: float = 1.0,
                 **kwargs):
        self.game = game
        self.deck = deck

        self.a = a
        self.scale = scale
        self.x, self.y = x, y 
        self.w, self.h = self.calculate_rotation(w,  h, self.a, self.scale)
        self.color = c

        self.tl = (self.x, self.y)
        self.bl = (self.x, self.y + self.h)
        self.tr = (self.x + self.w, self.y)
        self.br = (self.x + self.w, self.y + self.h)   
        
        hand_x = self.x + self.w // 2
        hand_y = self.y + self.h // 2
        self.hand = Hand(player=self, x=hand_x, y=hand_y, a=self.a, scale=self.scale)
    
        # self.detail = pygame.sprite.GroupSingle()
    
    def calculate_rotation(self, x, y, angle, scale):
        angle_radians = angle * pi / 180
        delta_x = x * cos(angle_radians) - y * sin(angle_radians)
        delta_y = x * sin(angle_radians) + y * cos(angle_radians)
        return delta_x * scale, delta_y * scale

    def update(self):
        self.hand.update()
        pygame.draw.polygon(self.game.screen.screen,
                            self.color,
                            [self.tl, self.tr, self.br, self.bl, self.tl],
                            width=1)

