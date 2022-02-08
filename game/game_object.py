import pygame
from typing import List


class Game:
    pass


class GameObject(pygame.sprite.Sprite):
    def __init__(self,
                 game: Game,
                 groups: List[pygame.sprite.Group] = None,
                 x=None,
                 y=None,
                 width=10,
                 height=10,
                 color=(255, 255, 255),
                 image: pygame.Surface = None,
                 scale=1.0):

        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.selected = False

        if image:
            size_to_set = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, size_to_set).convert_alpha()
            self.image = image
        else:
            self.image = pygame.Surface([width, height])
            self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x if x else 0
        self.rect.y = y if y else 0
        self.rect.center = (self.rect.x, self.rect.y)

        if groups is not None:
            for group in groups:
                group.add(self)

    def change_scale(self, scale):
        size_to_set = (int(self.image.get_width() * scale), int(self.image.get_height() * scale))
        image = pygame.transform.scale(self.image, size_to_set).convert_alpha()
        self.image = image
        self.rect = self.image.get_rect()

    def update(self) -> None:
        self.game.screen.screen.blit(pygame.transform.flip(self.image, flip_x=False, flip_y=False),
                                     (self.rect.x, self.rect.y))

        if self.selected:
            pygame.draw.rect(self.game.screen.screen, (0, 255, 0), self.rect, width=1)
