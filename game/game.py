import pygame
from game.card.card_detail_view import CardDetailView
from game.hardware import Keyboard, Mouse, Screen
from game.player import Player
from game.piles.deck import download_all_decks_images
from typing import List


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
        download_all_decks_images()
        pygame.init()
        self.screen = Screen(tittle='mtg_battle', width=1200, height=600)
        self.mouse = Mouse(game=self)
        self.keyboard = Keyboard(game=self)
        self.running = True
        self.players.append(Player(game=self, deck='Reap the Tides',
                                   scale=1, c=(0, 0, 0),
                                   x=0, y=self.screen.height//2,
                                   w=self.screen.width, h=self.screen.height//2, a=0.0))
        self.players.append(Player(game=self, deck='Lorehold Legacies',
                                   scale=1, c=(0, 255, 0),
                                   x=self.screen.width, y=self.screen.height//2,
                                   w=self.screen.width, h=self.screen.height//2, a=180.0))

        CardDetailView(name='Rout', game=self, x=0, y=0)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

            else:
                self.keyboard.keyboard_clicked(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse.mouse_up(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse.mouse_down(event)

    def handle_events(self):
        for event in pygame.event.get():
            self.on_event(event)

    def update(self):
        self.screen.screen.fill(self.screen.background_color)
        self.mouse.update()
        [player.update() for player in self.players]
        self.sprite_group.update()
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
