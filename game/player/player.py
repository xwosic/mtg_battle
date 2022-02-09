from game.player.lands import Lands
from game.player.battlefield import Battlefield
from game.player.zone import Zone
from .hand import Hand
from typing import Callable
from game.piles import Pile, Deck


class Game:
    pass


class Player(Zone):
    """
    Player class has to provide scalable and easy to rotate map of containers on screen.

    There will be couple of sprite groups to handle this:
        Hand
        Battlefield
            Arena
            Lands
        Graveyard
        Exile
        View (many cards with search)
        Detail (one card when hover over)
        Air (during drag ang drop)

    Player will get rotation angle and rectangle to "fit in", also each player will have his/her own deck.
    """
    def __init__(self, deck: str, **kwargs):
        super().__init__(**kwargs)
        self.lands = self.create_cardzone(Hand, x_ratio=0.25, y_ratio=0.3, w_ratio=0.75, h_ratio=0.3, **kwargs)
        self.hand = self.create_cardzone(Lands, x_ratio=0.25, y_ratio=0.6, w_ratio=0.75, h_ratio=0.3, **kwargs)
        self.battlefield = self.create_cardzone(Battlefield, x_ratio=0, y_ratio=0, w_ratio=1, h_ratio=0.3, **kwargs)
        self.zones = [self.lands, self.hand, self.battlefield]

        self.deck = self.create_deck(deck_name=deck, x_ratio=0.17, y_ratio=0.8, **kwargs)
        self.graveyard = self.create_pile(x_ratio=0.05, y_ratio=0.8, **kwargs)
        self.exile = self.create_pile(x_ratio=0.05, y_ratio=0.5, **kwargs)
        self.command_zone = self.create_pile(x_ratio=0.17, y_ratio=0.5, **kwargs)
        self.piles = [self.deck, self.graveyard, self.exile, self.command_zone]

    def calculate_position(self,
                           x_ratio: float,
                           y_ratio: float,
                           w_ratio: float = 1.0,
                           h_ratio: float = 1.0,
                           **kwargs):
        """
        Calculate position when player is rotated.
        """
        if self.is_rotated():
            x_ratio, y_ratio = y_ratio, x_ratio

        zone_x = self.x + int(self.w * x_ratio)
        zone_y = self.y + int(self.h * y_ratio)
        zone_w = int(kwargs['w'] * w_ratio)
        zone_h = int(kwargs['h'] * h_ratio)
        return {'x': zone_x, 'y': zone_y, 'w': zone_w, 'h': zone_h, 'a': self.a}

    def create_cardzone(self,
                        zone_type: Callable,
                        x_ratio: float,
                        y_ratio: float,
                        w_ratio: float,
                        h_ratio: float,
                        c: int,
                        **kwargs):
        """
        Creates CardZone based on player's width and hieght ratio.
        Requires w and h in kwargs.
        """
        return zone_type(**self.calculate_position(x_ratio, y_ratio, w_ratio, h_ratio, **kwargs),
                         c=c,
                         player=self,
                         game=self.game)

    def create_deck(self,
                    deck_name: str,
                    x_ratio: float,
                    y_ratio: float,
                    **kwargs):
        deck_position = self.calculate_position(x_ratio, y_ratio, **kwargs)
        return Deck(game=self.game,
                    player=self,
                    groups=[self.game.sprite_group],
                    name=deck_name,
                    color=self.color,
                    x=deck_position['x'],
                    y=deck_position['y'])

    def create_pile(self,
                    x_ratio: float,
                    y_ratio: float,
                    **kwargs):
        deck_position = self.calculate_position(x_ratio, y_ratio, **kwargs)
        return Pile(game=self.game,
                    groups=[self.game.sprite_group],
                    color=self.color,
                    x=deck_position['x'],
                    y=deck_position['y'])

    def update(self):
        [zone.update() for zone in self.zones]
        return super().update()
