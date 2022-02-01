import pygame
from game.game_object import GameObject
from typing import List
from pathlib import Path


class Card(GameObject):
    def __init__(self, 
                 name: str, 
                 default_path: str = 'cards',
                 **kwargs):
        self.name = name
        image = self.find_image(default_path, name)
        super().__init__(image=image, **kwargs)

    def find_image(self, default_path: str, name: str):
        path_to_card = Path.joinpath(Path(default_path), f'{name}.jpg')
        return pygame.image.load(path_to_card)