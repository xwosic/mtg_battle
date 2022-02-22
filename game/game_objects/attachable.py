from game.game_objects.dragable import Dragable


class Attachable(Dragable):
    def __init__(self, offset=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.attach_offset = offset
        self.is_attached = False

    def attach(self):
        self.game.mouse.method_on_select = self.attach_me_to_card

    def attach_me_to_card(self, card):
        self.loc = card
        self.is_attached = True
        self.right_click_options.pop('attach')
        self.right_click_options['detach'] = {'instance': self, 'kwargs': {}}

    def detach(self):
        self.loc = self.loc.loc
        self.is_attached = False
        self.right_click_options.pop('detach')
        self.right_click_options['attach'] = {'instance': self, 'kwargs': {}}

    def update(self):
        if self.is_attached:
            card_x, card_y = self.loc.rect.center
            self.rect.x = card_x + self.attach_offset[0]
            self.rect.y = card_y + self.attach_offset[1]

        super().update()
