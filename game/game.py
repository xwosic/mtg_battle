from turtle import width
from typing import Tuple
from game.deck import Deck
from game.card import Card
from game.mouse import Mouse
from game.screen import Screen
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
        self.players = []

    def on_init(self):
        pygame.init()
        self.screen = Screen(tittle='mtg_battle', width=1600)
        self.mouse = Mouse(game=self)
        self.running = True
        c1 = Card(groups=[self.sprite_group], name='Angel of the Ruins', x=300, y=50)
        c2 = Card(groups=[self.sprite_group], name='Arcane Denial', x=200, y=50)
        d1 = Deck(groups=[self.sprite_group], name='Reap the Tides', color=(0, 255, 255))

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