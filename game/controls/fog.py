from game.game_objects.clickable import Clickable
from game.game_objects.game_object import GameObject
from typing import List


class Fog(Clickable):
    def __init__(self, alpha=128, victims: List[GameObject] = [], **kwargs):
        super().__init__(**kwargs)
        self.change_image_alpha(alpha)
        self.victims = victims

    def left_upclick(self, **kwargs):
        """
        Disapear on click.
        Cancels 'transaction'.
        """
        for victim in self.victims:
            victim.kill()

        self.kill()
        return super().left_upclick(**kwargs)

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
