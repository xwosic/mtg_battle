import pygame
from game.clickable import Clickable
from game.game_object import GameObject
from typing import List


class Game:
    pass


class Dropdown(GameObject):
    def __init__(self, options: dict, **kwargs):
        super().__init__(**kwargs)
        mapping = self.create_mapping(options)
        print(mapping)
        self.options: List[Clickable] = []

    def create_mapping(self, options: dict):
        """
        in:
            options = {'class': Callable, 'options': List[str]}

        out:
            mapping = {<method name>: <method object>, ...}
        """
        mapping = {}
        class_obj = options['class']
        for option_name in options['options']:
            mapping[option_name] = class_obj.__getattribute__(option_name)

        return mapping

    def update(self) -> None:
        super().update()
        [option.update() for option in self.options]
