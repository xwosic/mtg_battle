"""
Example:
    Following code will create button to draw card on each click

    Dropdown(game=<Game>,
             groups=[<Game>.sprite_group],
             options={
                 'options': {
                     'draw': {'instance': <Game>.players[0].deck}
                 }
             }
    )

"""
from game.controls.button import Button
from game.controls.value_button import ValueButton
from game.game_objects import GameObject
from typing import List


class Game:
    pass


class Dropdown(GameObject):
    def __init__(self, options: dict, button_w=200, button_h=100, **kwargs):
        super().__init__(**kwargs)
        mapping = self.create_mapping(options)
        self.buttons = self.create_buttons(mapping)
        self.distribute_buttons(self.buttons, button_w, button_h)
        self.victims = self.buttons

    def create_mapping(self, options: dict):
        """
        in:
            options = {'method_name': {'instance': <class instance>, 'kwargs': {<kwargs>}'}}

        out:
            mapping = {<method name>: {'method': <method object>, 'kwargs': {...}}, ...}
        """
        mapping = {}
        for method_name, option_dict in options.items():
            mapping[method_name] = {'method': getattr(option_dict['instance'], method_name),
                                    'kwargs': option_dict['kwargs']}

        return mapping

    def create_buttons(self, mapping: dict) -> List[Button]:
        buttons = []
        for method_name, method_dict in mapping.items():
            if method_dict['kwargs']:
                buttons.append(ValueButton(parent=self,
                                           option_title=method_name,
                                           option_method=method_dict['method'],
                                           method_kwargs=method_dict['kwargs'],
                                           game=self.game,
                                           groups=[self.game.sprite_group]))
            else:
                buttons.append(Button(parent=self,
                                      option_title=method_name,
                                      option_method=method_dict['method'],
                                      method_kwargs=method_dict['kwargs'],
                                      game=self.game,
                                      groups=[self.game.sprite_group]))

        return buttons

    def distribute_buttons(self, buttons: List[Button], button_w: int, button_h: int):
        """
        Gives shape and places buttons in rectangle space.
        """
        self.rect.x = (self.game.screen.width - button_w) // 2
        self.rect.y = (self.game.screen.height - len(self.buttons) * button_h) // 2

        for number, button in enumerate(buttons):
            button.rect.x = self.rect.x
            button.rect.y = self.rect.y + number * button_h
            button.rect.width = button_w
            button.rect.height = button_h
            button.adapt_to_new_size()

        self.rect.width = button_w
        self.rect.height = len(buttons) * button_h
        self.adapt_to_new_size()

    def kill(self):
        """
        When dropdown is killed, it removes it's buttons.
        """
        for victim in self.victims:
            victim.kill()

        super().kill()

    def update(self) -> None:
        super().update()
        [button.update() for button in self.buttons]
