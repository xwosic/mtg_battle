from game.deck import Deck
from game.player.zone import Zone
from .hand import Hand
from typing import Callable
from math import cos, sin, pi


class Game:
    pass


class Player(Zone):
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
    def __init__(self, deck: Deck, **kwargs):
        super().__init__(**kwargs)
        self.deck = deck
        kwargs.pop('c')
        self.lands = self.create_cardzone(Hand, x_ratio=0.5, y_ratio=0.5, w_ratio=0.5, h_ratio=0.25, c=(255,0,0), **kwargs)
        self.hand = self.create_cardzone(Hand, x_ratio=0.5, y_ratio=0.75, w_ratio=0.5, h_ratio=0.25, c=(0,255,0), **kwargs)
        
        # self.detail = pygame.sprite.GroupSingle()
    
    def create_cardzone(self,
                        zone_type: Callable, 
                        x_ratio: float, 
                        y_ratio: float,
                        w_ratio: float,
                        h_ratio: float,
                        c: int,
                        **kwargs):
        """
        Creates CardZone based on player's width and hieght ratio.
        Requires w and h in kwargs.
        """
        if self.a == 0:
            pass
        elif self.a == 90 or self.a == 270:
            x_ratio, y_ratio = y_ratio, x_ratio

        zone_x = self.x + int(self.w * x_ratio)
        zone_y = self.y + int(self.h * y_ratio)
        zone_w = int(kwargs['w'] * w_ratio)
        zone_h = int(kwargs['h'] * h_ratio)
        print(f'player: {self.a} x:{self.x} y:{self.y} w:{int(self.w)} h:{int(self.h)} | x:{zone_x} y:{zone_y} w:{zone_w} h:{zone_h}')
        return zone_type(player=self, 
                         game=self.game,
                         x=zone_x,
                         y=zone_y,
                         w=zone_w,
                         h=zone_h,
                         a=self.a,
                         c=c,
                         scale=self.scale)

    def update(self):
        self.hand.update()
        self.lands.update()
        return super().update()
