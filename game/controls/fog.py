from game.game_objects.clickable import Clickable
from game.game_objects.game_object import GameObject
from typing import List


class Fog(Clickable):
    def __init__(self, alpha=128, victims: List[GameObject] = [], action_on_kill=None, **kwargs):
        super().__init__(**kwargs)
        self.change_image_alpha(alpha)
        self.victims = victims
        self._action_on_kill = action_on_kill

    def left_upclick(self, **kwargs):
        """
        Disapear on click.
        Performs actions and kills related objects.
        Cancels 'transaction'.
        """
        if self._action_on_kill:
            if isinstance(self._action_on_kill, list):
                for action in self._action_on_kill:
                    action()

            else:
                self._action_on_kill()

        for victim in self.victims:
            victim.kill()

        self.kill()
        return super().left_upclick(**kwargs)

    @property
    def action_on_kill(self):
        return self._action_on_kill

    @action_on_kill.setter
    def action_on_kill(self, value):
        """
        If action_on_kill is a list - append or extend,
        else overwrite.
        """
        if isinstance(self._action_on_kill, list):
            if isinstance(value, list):
                self._action_on_kill.extend(value)
            else:
                self._action_on_kill.append(value)

        else:
            self._action_on_kill = value

    @classmethod
    def full_screen_fog(cls, game):
        """
        Standard Fog factory.
        """
        kwargs = {
            'game': game,
            'groups': [game.sprite_group],
            'alpha': 127,
            'x': game.screen.width // 2,
            'y': game.screen.height // 2,
            'width': game.screen.width,
            'height': game.screen.height,
            'color': (0, 0, 0)
        }

        return cls(**kwargs)
