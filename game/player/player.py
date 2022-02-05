from math import cos, sin, pi
import pygame
from game.deck import Deck
from game.player.zone import Zone
from .hand import Hand


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

        hand_x = self.x + self.w // 2
        hand_y = self.y + self.h // 2
        self.hand = Hand(player=self, x=hand_x, y=hand_y, a=self.a, scale=self.scale)
    
        # self.detail = pygame.sprite.GroupSingle()
