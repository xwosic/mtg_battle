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
                 width=100,
                 height=100,
                 rotation_angle: float = 0.0,
                 scale: float = 1.0,
                 **kwargs):
        self.game = game
        self.deck = deck
        self.x = x
        self.y = y
        self.width = width
        self.height = height  
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)      
        self.rotation_angle = rotation_angle
        self.scale = scale
        self.hand = Hand(player=self, x=x, y=y, rotation_angle=rotation_angle, scale=scale)
        # self.detail = pygame.sprite.GroupSingle()
    
    def update(self):
        self.hand.update()
        pygame.draw.rect(self.game.screen.screen, (255, 0, 0), self.rect, width=1)

