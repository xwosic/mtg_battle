import pygame


class Game:
    # world phisics variables
    GRAVITY = 1
    # camera variables
    FOLLOW_PLAYER = False
    # tiles world
    SCALE = 0.75
    ROWS = 16
    COLUMNS = 150
    TILE_SIZE = None
    TILE_TYPES_NUM = 21
    CURRENT_LVL = 1
    WORLD_MAP = []
    # fonts
    TEXT_FONT = None
    GREEN = (0, 255, 0)

    def __init__(self):
        # screen
        self.width = 800
        self.heigth = int(self.width * 0.8)
        self.size = (self.width, self.heigth)
        self.background_color = (100, 100, 100)
        self.TILE_SIZE = self.heigth // self.ROWS
        # time
        self.clock = pygame.time.Clock()
        self.FPS = 30
        # states
        self.running = False
        self.states = {
            'moving_right': False,
            'moving_left': False,
            'jump': False,
            'attack': False,
            'spell': False,
        }
        # jump, left, right, space, granade
        self.pressed_keys = {
            'up': False,
            'left': False,
            'right': False,
            'space': False,
            'f': False
        }
        # everything is in sprite_group
        self.sprite_group = pygame.sprite.Group()

        # pointer to player
        self.player = None

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('mtg_battle')
        self.running = True
        self.TEXT_FONT = pygame.font.SysFont('calibri', 15)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.states['moving_left'] = True
                # self.pressed_keys['left'] = True

            if event.key == pygame.K_RIGHT:
                self.states['moving_right'] = True
                # self.pressed_keys['right'] = True

            if event.key == pygame.K_UP:
                self.states['jump'] = True
                # self.pressed_keys['up'] = True

            if event.key == pygame.K_SPACE:
                self.states['attack'] = True
                # self.pressed_keys['space'] = True
            
            if event.key == pygame.K_f:
                self.states['spell'] = True
                # self.pressed_keys['f'] = True

            if event.key == pygame.K_ESCAPE:
                self.running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.states['moving_left'] = False
                # self.pressed_keys['left'] = False

            if event.key == pygame.K_RIGHT:
                self.states['moving_right'] = False
                # self.pressed_keys['right'] = False
            
            if event.key == pygame.K_SPACE:
                self.states['attack'] = False
                # self.pressed_keys['space'] = False
        
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

    def draw_text(self, text, font=None, text_color=(0, 0, 0), x=0, y=0):
        if font == None:
            font = self.TEXT_FONT

        img = self.TEXT_FONT.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def execute(self):
        if not self.running:
            self.on_init()

        while self.running:
            self.clock.tick(self.FPS)
            self.handle_events()
            self.update()

        self.clean_up()