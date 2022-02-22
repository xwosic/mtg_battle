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
from game.game_objects import Attachable


class DiceCounter(Attachable):
    def __init__(self, init_value=1, reversed=False, **kwargs):
        super().__init__(**kwargs)
        try:
            init_value = int(init_value)
        except ValueError:
            init_value = 1

        self.value = init_value
        self.reversed = reversed
        self.text = self.value_to_text()
        self.font = pygame.font.Font(None, 32)
        self.default_drops = ['CardVisualization', 'Anywhere']
        self.render_text()

    def increment(self):
        if self.reversed:
            self.value -= 1
        else:
            self.value += 1
        self.value_to_text()
        self.render_text()

    def decrement(self):
        if self.reversed:
            self.value += 1
        else:
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

    @classmethod
    def create_card_counter(cls, card, init_value: int):
        number_of_counters = len([counter for counter in card.attached_things if isinstance(counter, DiceCounter)])
        offset_x = card.rect.width // 4 * 3
        quarter_of_height = card.rect.height // 4
        offset_y = - quarter_of_height * (number_of_counters)
        offset = (offset_x, offset_y)
        dice = cls(init_value=init_value,
                   reversed=True,
                   game=card.game,
                   groups=[card.game.sprite_group],
                   width=20,
                   height=20)
        dice.attach_me_to_card(card, offset=offset)
