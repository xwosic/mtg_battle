class Card:
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(width, height, **kwargs)
        self.rect.x = x
        self.rect.y = y

    def add_gravity(self, game):
        pass

    def collide_with_tiles(self, game):
        pass

    def get_hit(self, demage, game):
        pass

    def prevent_collisions(self, game):
        pass