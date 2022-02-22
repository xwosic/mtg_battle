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

import pygame
from game.game_objects import Dragable


class DiceCounter(Dragable):
    def __init__(self, init_value=1, **kwargs):
        super().__init__(**kwargs)
        self.value = init_value
        self.text = self.value_to_text()
        self.font = pygame.font.Font(None, 32)
        self.default_drops = ['CardVisualization', 'Anywhere']
        self.render_text()

    def increment(self):
        self.value += 1
        self.value_to_text()
        self.render_text()

    def decrement(self):
        self.value -= 1
        self.value_to_text()
        self.render_text()

    def left_upclick(self, **kwargs):
        self.decrement()
        return super().left_upclick(**kwargs)

    def right_upclick(self, **kwargs):
        self.increment()
        return super().right_upclick(**kwargs)

    def value_to_text(self):
        self.text = str(self.value)
        return self.text

    def render_text(self):
        self.image.fill(self.color)
        self.draw_text(text=self.text)
