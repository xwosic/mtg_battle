from game.zones.card_zone import CardZone
from game.card import Card, CardVisualization
from typing import List


class CardView(CardZone):
    def __init__(self, pile, **kwargs):
        self.pile = pile
        super().__init__(**kwargs)

    def create_view(self, cards_names: List[str]):
        self.kill()
        for name in cards_names:
            card = Card(game=self.game, name=name)
            card.loc = self
            self.add_card(card)

    def remove_card(self, card: CardVisualization):
        self.pile.remove_card(card.name)
        return super().remove_card(card)

    def kill(self):
        # on delete remove all cards
        for card in self.cards:
            card.kill()
