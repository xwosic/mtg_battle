from .card_zone import CardZone


class Player:
    pass


class Lands(CardZone):
    def __init__(self, player: Player, **kwargs):
        self.player = player
        super().__init__(**kwargs)
