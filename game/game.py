from typing import Tuple
from game.deck import Deck
from game.card import Card
from game.mouse import Mouse
import pygame


class Game:
    def __init__(self):
        # screen
        self.screen: pygame.Surface = None
        self.text_font: pygame.font.Font = None
        self.width = 1200
        self.heigth = int(self.width * 0.8)
        self.size: Tuple[int, int] = (self.width, self.heigth)
        self.background_color: Tuple[int, int, int] = (100, 100, 100)
        # time
        self.clock = pygame.time.Clock()
        self.FPS = 30
        # states
        self.running = False
        # everything is in sprite_group
        self.sprite_group = pygame.sprite.Group()
        # pointers to players
        self.players = []

    def draw_text(self, text, font=None, text_color=(0, 0, 0), x=0, y=0):
        if font == None:
            font = self.text_font

        img = self.text_font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('mtg_battle')
        self.text_font = pygame.font.SysFont('calibri', 15)
        self.running = True
        self.mouse = Mouse(game=self)
        c1 = Card(groups=[self.sprite_group], name='Angel of the Ruins', x=300, y=50)
        c2 = Card(groups=[self.sprite_group], name='Arcane Denial', x=200, y=50)
        d1 = Deck(groups=[self.sprite_group], name='Reap the Tides', color=(0, 255, 255))
        print(d1.cards)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse.mouse_up(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse.mouse_down(event)
        
    def handle_events(self):
        for event in pygame.event.get():
            self.on_event(event)

    def update(self):
        self.screen.fill(self.background_color)
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