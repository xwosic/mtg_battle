import pygame
from typing import List


class GameObject(pygame.sprite.Sprite):
    def __init__(self,
                 groups: List[pygame.sprite.Group] = None,
                 x=None,
                 y=None,
                 width=10,
                 height=10,
                 color=(255, 255, 255),
                 image=None):

        pygame.sprite.Sprite.__init__(self)
        self.selected = True

        if image:
            self.image = image
        else:
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
        
        self.rect = self.image.get_rect()

        self.rect.x = x if x else 0
        self.rect.y = y if y else 0

        if groups is not None:
            for group in groups:
                group.add(self)

    def update(self, game) -> None:
        game.screen.blit(pygame.transform.flip(self.image, flip_x=False, flip_y=False),
                        (self.rect.x, self.rect.y))

        if self.selected:
            pygame.draw.rect(game.screen, (0, 255, 0), self.rect, width=1)