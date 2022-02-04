import pygame

class Player:
    pass


class Hand:
    def __init__(self, 
                 player: Player, 
                 x=0, 
                 y=0, 
                 w=100,
                 h=10,
                 a=0.0,
                 scale=1.0,
                 **kwargs):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.a = a
        self.tl = (self.x, self.y)
        self.bl = (self.x, self.y + self.h)
        self.tr = (self.x + self.w, self.y)
        self.br = (self.x + self.w, self.y + self.h)
        self.player = player
        self.cards = pygame.sprite.Group()
    
    def distribute(self):
        """
        Change coordinates of each card in this zone to distribute them equaly.
        """
        cards_count = len(self.cards)
        space_x = self.w // (cards_count + 1)
        space_y = self.h // (cards_count + 1)
        for number, card in enumerate(self.cards):
            card.rect.x = self.rect.x + space_x * (number + 1)
            card.rect.y = self.rect.y + space_y * (number + 1)
    
    def update(self):
        self.distribute()
        self.cards.update(self.player.game)
        pygame.draw.polygon(self.player.game.screen.screen,
                            (255, 0, 0),
                            [self.tl, self.tr, self.br, self.bl, self.tl],
                            width=1)