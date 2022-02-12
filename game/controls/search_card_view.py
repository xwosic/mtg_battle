"""
create fog
get cards from pile
filter cards with search box
drag cards from view to board
"""

from game.controls.fog import Fog
from .input_box import InputBox
from .view import CardView


class SearchCardView:
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
        self.search_box = InputBox(game=self.game,
                                   always_send=True,
                                   send_to_callable=self.pile.match_card_name,
                                   send_call_result_to=self.view.create_view,
                                   x=self.game.screen.width // 2,
                                   y=self.game.screen.height // 4,
                                   width=200,
                                   height=50)

        self.fog.kill_with_me = [self.search_box, self.view]

        # activate search box
        self.search_box.left_upclick()
        # get all cards
        cards = self.pile.match_card_name('')
        # and display then
        self.view.create_view(cards)
