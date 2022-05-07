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
import random
from game.game_objects import Attachable
from game.game_objects.clickable import Clickable


class DiceCounter(Attachable):
    def __init__(self, init_value=1, reversed=False, number=0, **kwargs):
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
        self.order_number = number
        self.card_width = 0
        self.card_height_quarter = 0
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

    def card_was_rotated(self):
        if self.loc:
            if self.loc.rect.width != self.card_width:
                self.card_width = self.loc.rect.width
                self.card_height_quarter = self.loc.rect.height // 4
                return True
        return False

    def update(self):
        if self.is_attached:
            if self.card_was_rotated():
                self.rect.width = self.card_width // 4
                self.rect.height = self.card_height_quarter
                self.adapt_to_new_size()
                self.render_text()
            self.rect.x = self.loc.rect.x + self.card_width
            self.rect.y = self.loc.rect.y + self.card_height_quarter * self.order_number
        # skipping Attachable.update method
        return super(Clickable, self).update()

    @classmethod
    def create_card_counter(cls, card, init_value: int):
        number_of_counters = len([counter for counter in card.attached_things if isinstance(counter, DiceCounter)])
        if number_of_counters < 4:
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            dice = cls(init_value=init_value,
                       reversed=True,
                       game=card.game,
                       groups=[card.game.sprite_group],
                       color=color,
                       number=number_of_counters)
            dice.attach_me_to_card(card)

    def detach(self):
        self.kill()
