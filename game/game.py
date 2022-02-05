from typing import List
from game.deck import Deck
from game.card import Card
from game.mouse import Mouse
from game.screen import Screen
from game.player import Player
import pygame


class Game:
    def __init__(self):
        # screen
        self.screen: Screen = None
        # time
        self.clock = pygame.time.Clock()
        self.FPS = 30
        # states
        self.running = False
        # everything is in sprite_group
        self.sprite_group = pygame.sprite.Group()
        # pointers to players
        self.players: List[Player] = []

    def on_init(self):
        pygame.init()
        self.screen = Screen(tittle='mtg_battle', width=1600)
        self.mouse = Mouse(game=self)
        self.running = True
        d = Deck(groups=[self.sprite_group], name='Reap the Tides', color=(0, 255, 255), x=10, y=10)
        self.players.append(Player(game=self, deck=d, scale=1, c=(0, 0, 0),   x=self.screen.width//2, y=self.screen.height//2, w=self.screen.width//2, h=self.screen.height//2, a=0.0))    # black
        self.players.append(Player(game=self, deck=d, scale=1, c=(255, 0, 0), x=self.screen.width//4, y=0, w=self.screen.height, h=self.screen.width//4, a=90.0))   # red
        self.players.append(Player(game=self, deck=d, scale=1, c=(0, 255, 0), x=self.screen.width, y=self.screen.height//2, w=self.screen.width//2, h=self.screen.height//2, a=180.0))  # green
        self.players.append(Player(game=self, deck=d, scale=1, c=(0, 0, 255), x=self.screen.width//4, y=self.screen.height, w=self.screen.height, h=self.screen.width//4, a=270.0))  # blue
        for n, p in enumerate(self.players):
            self.add_cards(n)

    def add_cards(self, num: int):
        self.players[num].hand.cards.add(Card(groups=[self.sprite_group], name='Angel of the Ruins').view)
        self.players[num].hand.cards.add(Card(groups=[self.sprite_group], name='Arcane Denial').view)
        self.players[num].hand.cards.add(Card(groups=[self.sprite_group], name='Forest').view)
        self.players[num].hand.cards.add(Card(groups=[self.sprite_group], name='Island').view)
        self.players[num].hand.cards.add(Card(groups=[self.sprite_group], name='Cleansing Nova').view)
        self.players[num].hand.cards.add(Card(groups=[self.sprite_group], name='Coiling Oracle').view)
        self.players[num].hand.cards.add(Card(groups=[self.sprite_group], name='Doomskar').view)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse.mouse_up(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse.mouse_down(event)
        
    def handle_events(self):
        for event in pygame.event.get():
            self.on_event(event)

    def update(self):
        self.screen.screen.fill(self.screen.background_color)
        # player update
        [player.update() for player in self.players]
        self.sprite_group.update(self)
        pygame.display.update()

    def clean_up(self):
        # save progress
        # to do
        # close game
        pygame.quit()

    def execute(self):
        if not self.running:
            self.on_init()

        while self.running:
            self.clock.tick(self.FPS)
            self.handle_events()
            self.update()

        self.clean_up()
