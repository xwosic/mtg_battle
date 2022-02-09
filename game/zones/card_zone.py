import pygame
from game.zones.zone import Zone
from game.card import Card, CardVisualization


class CardZone(Zone):
    def __init__(self, **kwargs):
        self.cards = pygame.sprite.Group()
        super().__init__(**kwargs)

    def add_card(self, card):
        if isinstance(card, CardVisualization):
            self.cards.add(card)
            # self.rotate_card_if_new(card)
            card.loc = self
            if len(self.cards) > 0:
                self.distribute_cards()

        elif isinstance(card, Card):
            self.cards.add(card.view)
            # self.rotate_card_if_new(card.view)
            card.view.loc = self
            if len(self.cards) > 0:
                self.distribute_cards()

    def remove_card(self, card: CardVisualization):
        if card in self.cards:
            self.cards.remove(card)
        return card.name

    def rotate_card_if_new(self, view):
        if view.loc is not self:
            print('its new me')
            if self.is_rotated():
                self.rotate_card(view)

    def rotate_card(self, view):
        position = view.rect.center
        view.image = pygame.transform.rotate(view.image, -self.a)
        view.rect = view.image.get_rect()
        view.rect.center = position

    def undo_rotate_card(self, view):
        position = view.rect.center
        view.image = pygame.transform.rotate(view.image, self.a)
        view.rect = view.image.get_rect()
        view.rect.center = position

    def distribute_cards(self):
        # count space between cards
        cards_count = len(self.cards)
        space_x = self.rect.width // (cards_count + 1)
        space_y = self.rect.height // (cards_count + 1)

        # map coordinates with objects
        coordinate_dict = {}
        for card in self.cards:
            for card in self.cards:
                if self.is_rotated():
                    coordinate_dict[card.rect.centery] = card
                else:
                    coordinate_dict[card.rect.centerx] = card

        # sort coordinates in ascending order
        list_of_order = list(coordinate_dict.keys())
        list_of_order.sort()

        # distribute
        for number, coordinate in enumerate(list_of_order):
            if self.is_rotated():
                coordinate_dict[coordinate].rect.centerx = self.rect.x + self.rect.width // 2
                coordinate_dict[coordinate].rect.centery = self.rect.y + space_y * (number + 1)
            else:
                coordinate_dict[coordinate].rect.centerx = self.rect.x + space_x * (number + 1)
                coordinate_dict[coordinate].rect.centery = self.rect.y + self.rect.height // 2
