from game.zones.card_zone import CardZone
from game.card import Card, CardVisualization
from typing import List


class CardView(CardZone):
    def __init__(self, pile, player=None, method_on_kill=None, **kwargs):
        """
        If player is set - view will overlap player's zones.
        If method_on_kill is set - cards' views will be send to a method on CardView kill.
        """
        self.pile = pile
        self.player = player
        self.method_on_kill = method_on_kill
        super().__init__(**kwargs)
        if self.player:
            self.player.zones.insert(0, self)

    def create_view(self, cards_names: List[str]):
        self.delete_cards()
        for name in cards_names:
            card = Card(game=self.game, name=name, x=self.game.screen.width, y=0)
            self.add_card(card)

    def remove_card(self, card: CardVisualization):
        self.pile.remove_card(card.name)
        return super().remove_card(card)

    def kill(self):
        if self.method_on_kill:
            self.sort_cards_from_left_to_right()
            self.method_on_kill(*self.cards)

        if self.player:
            self.player.zones.remove(self)

        for card in self.cards:
            card.kill()

    def delete_cards(self):
        # on delete remove all cards
        for card in self.cards:
            card.kill()

    def sort_cards_from_left_to_right(self):
        """
        Cards order is the order of adding to list.
        Changes this order to order from left to right.
        Left on bottom, right on top.
        """
        coordinates = {}
        for card in self.cards:
            coordinates[card.rect.x] = card

        list_of_order = list(coordinates.keys())
        list_of_order.sort()
        self.cards = [coordinates[card_coords] for card_coords in list_of_order]
