"""
create fog
get tokens from pile
drag cards from view to board
"""

from game.controls.fog import Fog
from .card_view import CardView


class TokenView:
    def __init__(self, game, pile):
        self.game = game
        self.pile = pile
        self.fog = Fog.full_screen_fog(self.game)
        self.view = CardView(game=self.game,
                             pile=self.pile,
                             x=0,
                             y=0,
                             w=self.game.screen.width,
                             h=self.game.screen.height)

        self.fog.victims = [self.view]

        # and display then
        self.view.create_view(self.pile.tokens)
