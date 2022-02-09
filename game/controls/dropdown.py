import pygame
from game.game_object import GameObject
from typing import List
from game.controls.button import Button


class Game:
    pass


class Dropdown(GameObject):
    def __init__(self, options: dict, **kwargs):
        super().__init__(**kwargs)
        mapping = self.create_mapping(options)
        self.options = self.create_buttons(mapping)
        print(mapping)

    def create_mapping(self, options: dict):
        """
        in:
            options = {'instance': <class instance>, 'options': List[str]}

        out:
            mapping = {<method name>: <method object>, ...}
        """
        class_instance = options['instance']
        mapping = {
            'instance': class_instance,
            'methods': {}
        }
        for option_name in options['options']:
            mapping['methods'][option_name] = class_instance.__getattribute__(option_name)

        return mapping

    def create_buttons(self, mapping: dict) -> List[Button]:
        buttons = []
        index = 0
        for method_name, method in mapping['methods'].items():
            buttons.append(Button(game=self.game,
                                  groups=[self.game.sprite_group],
                                  y=index*15,
                                  option_title=method_name,
                                  option_method=method,
                                  instance=mapping['instance']))
            index += 1

        return buttons

    def update(self) -> None:
        super().update()
        [option.update() for option in self.options]
