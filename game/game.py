import pygame
from game.controls.dropdown import Dropdown
from game.mouse import Mouse
from game.player import Player
from game.screen import Screen
from typing import List
from game.controls.fog import Fog


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
        self.screen = Screen(tittle='mtg_battle', width=1200, height=600)
        self.mouse = Mouse(game=self)
        self.running = True
        self.players.append(Player(game=self, deck='Reap the Tides',
                                   scale=1, c=(0, 0, 0),
                                   x=0, y=self.screen.height//2,
                                   w=self.screen.width, h=self.screen.height//2, a=0.0))
        # self.players.append(Player(game=self, deck='Lorehold Legacies',
        #                            scale=1, c=(255, 0, 0),
        #                            x=self.screen.width//2, y=0,
        #                            w=self.screen.height, h=self.screen.width//2, a=90.0))
        self.players.append(Player(game=self, deck='Lorehold Legacies',
                                   scale=1, c=(0, 255, 0),
                                   x=self.screen.width, y=self.screen.height//2,
                                   w=self.screen.width, h=self.screen.height//2, a=180.0))
        # self.players.append(Player(game=self, deck='Reap the Tides',
        #                            scale=1, c=(0, 0, 255),
        #                            x=self.screen.width//2, y=self.screen.height,
        #                            w=self.screen.height, h=self.screen.width//2, a=270.0))

        f = Fog(game=self, groups=[self.sprite_group], alpha=127, x=self.screen.width//2, y=self.screen.height//2,
                width=self.screen.width, height=self.screen.height, color=(0, 0, 0))
        d = Dropdown(game=self, groups=[self.sprite_group],
                     options={'instance': self.players[0].deck, 'options': {'draw': {}}})
        f.kill_with_me = [d]

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
