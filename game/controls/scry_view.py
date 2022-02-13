from game.controls.fog import Fog
from .input_box import InputBox
from .card_view import CardView


class ScryView:
    def __init__(self, game, player, pile):
        self.game = game
        self.player = player
        self.pile = pile
        self.fog = Fog.full_screen_fog(self.game)
        self.view = CardView(game=self.game,
                             pile=self.pile,
                             player=player,
                             x=0,
                             y=0,
                             w=self.game.screen.width,
                             h=self.game.screen.height)
        self.view_bottom_cards = CardView(game=self.game,
                                          pile=self.pile,
                                          player=self.player,
                                          method_on_kill=self.pile.view.put_card_on_bottom,
                                          x=self.game.screen.width//5,
                                          y=self.game.screen.height//2,
                                          w=self.game.screen.width//5,
                                          h=self.game.screen.height//5,
                                          c=(255, 0, 0))
        self.view_top_cards = CardView(game=self.game,
                                       pile=self.pile,
                                       player=self.player,
                                       method_on_kill=self.pile.view.put_card_on_top,
                                       x=self.game.screen.width//5 * 3,
                                       y=self.game.screen.height//2,
                                       w=self.game.screen.width//5,
                                       h=self.game.screen.height//5,
                                       c=(0, 255, 0))
        self.search_box = InputBox(game=self.game,
                                   send_to_callable=self.pile.scry,
                                   send_call_result_to=self.view.create_view,
                                   x=self.game.screen.width // 2,
                                   y=self.game.screen.height // 4,
                                   width=200,
                                   height=50)

        self.fog.victims = [self.search_box, self.view, self.view_bottom_cards, self.view_top_cards]

        # activate search box
        self.search_box.left_upclick()
