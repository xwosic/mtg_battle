from .card_zone import CardZone


class Player:
    pass


class Hand(CardZone):
    def __init__(self, player: Player, **kwargs):
        self.player = player
        super().__init__(**kwargs)

    def shuffle_hand_into_library(self):
        for card_view in self.cards:
            self.remove_card(card_view)
            self.player.deck.view.put_card_on_top(card_view)

        self.player.deck.shuffle()
