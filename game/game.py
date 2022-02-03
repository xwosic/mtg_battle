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
        d = Deck(groups=[self.sprite_group], name='Reap the Tides', color=(0, 255, 255), x=100, y=100)
        Card(groups=[self.sprite_group], name='Forest', x=135, y=650, scale=0.7)
        Card(groups=[self.sprite_group], name='Forest', x=235, y=650, scale=0.7)
        Card(groups=[self.sprite_group], name='Forest', x=335, y=650, scale=0.7)
        Card(groups=[self.sprite_group], name='Forest', x=435, y=650, scale=0.7)
        Card(groups=[self.sprite_group], name='Forest', x=535, y=650, scale=0.7)
        Card(groups=[self.sprite_group], name='Island', x=635, y=650, scale=0.7)
        Card(groups=[self.sprite_group], name='Island', x=735, y=650, scale=0.7)
        Card(groups=[self.sprite_group], name='Island', x=835, y=650, scale=0.7)
        Card(groups=[self.sprite_group], name='Island', x=935, y=650, scale=0.7)
        self.players.append(Player(game=self, deck=d, x=250, y=250))
        self.players[0].hand.cards.add(Card(groups=[self.sprite_group], name='Angel of the Ruins').view)
        self.players[0].hand.cards.add(Card(groups=[self.sprite_group], name='Arcane Denial').view)

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
