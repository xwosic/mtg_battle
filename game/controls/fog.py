from game.clickable import Clickable
from game.game_object import GameObject
from typing import List


class Fog(Clickable):
    def __init__(self, alpha=128, victims: List[GameObject] = [], **kwargs):
        super().__init__(**kwargs)
        self.change_image_alpha(alpha)
        self.kill_with_me = victims

    def left_upclick(self, **kwargs):
        """
        Disapear on click.
        Cancels 'transaction'.
        """
        for victim in self.kill_with_me:
            victim.kill()

        self.kill()
        return super().left_upclick(**kwargs)
