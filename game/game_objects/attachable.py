from game.game_objects.dragable import Dragable


class Attachable(Dragable):
    def __init__(self, offset=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.right_click_options['attach'] = {'instance': self, 'kwargs': {}}
        self.attach_offset = offset
        self.is_attached = False
        self.attached_things = []

    def attach(self):
        """
        When dropdown button is clicked.
        Mouse has method set to run on next click.
        """
        self.game.mouse.method_on_select = self.attach_me_to_card

    def attach_me_to_card(self, card, offset=None):
        """
        Check if card is not attaching to itself
        and if card is not in things attached to itself (circular attachment).
        If not - set loc to card and change options.
        """
        if card is not self:
            if card not in self.attached_things:
                self.loc = card
                self.loc.attached_things.append(self)
                self.is_attached = True

                # change dropdown options
                self.right_click_options.pop('attach')
                self.right_click_options['detach'] = {'instance': self, 'kwargs': {}}

                # set offset
                if offset:
                    self.attach_offset = offset
                else:
                    self.attach_offset = (card.rect.width // 2, card.rect.height // 2)

    def detach(self):
        """
        Change loc to loc of card attached to and change options.
        """
        self.loc = self.loc.loc
        self.is_attached = False
        self.right_click_options.pop('detach')
        self.right_click_options['attach'] = {'instance': self, 'kwargs': {}}

    def update(self):
        """
        Attached thing will be following card to which it is attached to.
        """
        if self.is_attached:
            self.rect.x = self.loc.rect.x + self.attach_offset[0]
            self.rect.y = self.loc.rect.y + self.attach_offset[1]

        super().update()
