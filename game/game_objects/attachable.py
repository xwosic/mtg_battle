from tapable import Tapable


class Attachable(Tapable):
    def __init__(self, offset=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.attach_offset = offset
        self.is_attached = False

    def attach(self, loc):
        self.loc = loc
        self.is_attached = True

    def deattach(self):
        self.loc = None
        self.is_attached = False

    def update(self):
        if self.is_attached:
            self.rect.topleft = self.loc.rect.center + self.attach_offset

        super().update()
