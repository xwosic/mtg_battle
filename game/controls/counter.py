"""
LPM: decrement
PPM: increment
drag: to delete in delete zone
drag: to relocate on card

on game start: each player has his/her life counter

Cards can have multiple Counters on themselfs:
    - add on PPM
    - list of counters
    - locate them on card
    - different random color (with posibility to set)

Applicable on cards and tokens and without them.
"""

from game.game_objects import Dragable


class DiceCounter(Dragable):
    def __init__(self, init_value=1, **kwargs):
        super().__init__(**kwargs)
        self._value = init_value
        self.text = str(self._value)
        self.default_drops = ['CardVisualization', 'Anywhere']

    def value_to_text(self):
        return str(self._value)

    def update(self) -> None:
        super().update()
        self.draw_text(text=self.text)

    @property
    def value(self) -> str:
        return self.text

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.text = self.value_to_text()
