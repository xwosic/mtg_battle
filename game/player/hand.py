import pygame

class Player:
    pass


class Hand:
    def __init__(self, player: Player, x=0, y=0, width=100, height=100, rotation_angle=0.0, scale=1.0, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.rotation_angle = rotation_angle
        self.player = player
        self.cards = pygame.sprite.Group()
    
    def distribute(self):
        """
        Change coordinates of each card in this zone to distribute them equaly.
        """
        cards_count = len(self.cards)
        space_x = self.width // (cards_count + 1)
        space_y = self.height // (cards_count + 1)
        for number, card in enumerate(self.cards):
            card.rect.x = self.rect.x + space_x * (number + 1)
            card.rect.y = self.rect.y + space_y * (number + 1)
    
    def update(self):
        self.distribute()
        self.cards.update(self.player.game)
        pygame.draw.rect(self.player.game.screen.screen, (255, 0, 0), self.rect, width=1)
