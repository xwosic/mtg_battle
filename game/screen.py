import pygame
from typing import Tuple


class Screen:
    def __init__(self,
                 tittle: str,
                 width: int,
                 height: int = None,
                 size: Tuple[int, int] = None,
                 text_font: pygame.font.Font = None,
                 background_color: Tuple[int, int, int] = (100, 100, 100)):
        # size
        self.width = width
        self.height = height if height else width // 2
        self.size = (self.width, self.height)
        if size is not None:
            self.size = size
            self.width = self.size[0]
            self.height = self.size[1]

        self.up_right_corner = (self.width, 0)
        self.up_left_corner = (0, 0)
        self.bottom_right_corner = (self.width, self.height)
        self.bottom_left_corner = (0, self.height)
        self.center = (self.width // 2, self.height // 2)

        # apperiance
        self.text_font = text_font if text_font else pygame.font.SysFont('calibri', 15)
        self.background_color = background_color

        # display
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(tittle)

    def draw_text(self, text, font=None, text_color=(0, 0, 0), x=0, y=0):
        if font is None:
            font = self.text_font

        img = self.text_font.render(text, True, text_color)
        self.screen.blit(img, (x, y))
