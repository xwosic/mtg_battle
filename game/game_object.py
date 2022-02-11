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
        self.color = color

        if image:
            size_to_set = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, size_to_set).convert_alpha()
            self.image = image
        else:
            self.image = pygame.Surface([width, height])
            self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = x if x else 0
        self.rect.y = y if y else 0
        self.rect.center = (self.rect.x, self.rect.y)

        if groups is not None:
            for group in groups:
                group.add(self)

    def adapt_to_new_size(self):
        """
        Fill new rect with color.
        """
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

    def change_scale(self, scale):
        """
        Change scale of image and rect without changing position. Loses img quality.
        """
        size_to_set = (int(self.image.get_width() * scale), int(self.image.get_height() * scale))
        image = pygame.transform.scale(self.image, size_to_set).convert_alpha()
        self.image = image
        position = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = position

    def draw_text(self, text, font=None, text_color=(0, 0, 0), x=0, y=0):
        """
        Write text on the middle of object.
        """
        if font is None:
            font = self.game.screen.text_font

        img = self.game.screen.text_font.render(text, True, text_color)

        img_half_w = img.get_width() // 2
        img_half_h = img.get_height() // 2
        x = x if x else self.rect.width // 2 - img_half_w
        y = y if y else self.rect.height // 2 - img_half_h

        self.image.blit(img, (x, y))

    def update(self) -> None:
        """
        Blit image to game screen. If selected, draw green border around.
        """
        self.game.screen.screen.blit(pygame.transform.flip(self.image, flip_x=False, flip_y=False),
                                     (self.rect.x, self.rect.y))

        if self.selected:
            pygame.draw.rect(self.game.screen.screen, (0, 255, 0), self.rect, width=1)
