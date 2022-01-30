import csv
from random import choices
import pygame
from game.loader import load_tiles


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
        # everything which can stop bullet is here
        self.touch_group = pygame.sprite.Group()
        # everything which support standing on it is here
        self.tile_group = pygame.sprite.Group()
        # enemy cannot shoot to each other
        self.enemy_group = pygame.sprite.Group()
        # pointer to player
        self.player = None
        # graphics showed on the screen
        self.bullet_graphic  = None
        self.grenade_graphic = None
        # load level
        # self.load_current_lvl()


    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('mtg_battle')
        self.running = True
        self.TEXT_FONT = pygame.font.SysFont('calibri', 15)
        # tiles
        # self.tiles_img = self.load_tiles_img('img/tile', scale=1.7 * self.SCALE)
        
        # init Classes used in game
        # Explosion.init(self.SCALE)
        # SmallExplosion.init(self.SCALE)

        # populate the world
        self.populate_world()
        # self.player = Player(self.width/2, self.heigth/2, groups=[self.sprite_group, self.touch_group], game=self)

    
    def load_current_lvl(self):
        # clear map
        self.WORLD_MAP = []
        for row in range(self.ROWS):
            r = [-1] * self.COLUMNS
            self.WORLD_MAP.append(r)

        # load data from csv
        with open(f'level{self.CURRENT_LVL}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.WORLD_MAP[x][y] = int(tile)


    def load_tiles_img(self, path, scale=1):
        """Scrapps all images to list from a given directory."""
        return load_tiles(path, scale=scale)

    
    def populate_world(self):
        for row, list in enumerate(self.WORLD_MAP):
            for col, img_num in enumerate(list):
                pass
                # if img_num >= 0:
                    # if img_num in [9, 10, 11, 13, 14, 20]:
                    #     # touchless
                    #     Tile(col * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE, self.tiles_img[img_num], groups=[self.sprite_group])
                    # elif img_num in [0, 1, 2, 3, 4, 5, 6, 7, 8, 12]:
                    #     # touchable
                    #     Tile(col * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE, self.tiles_img[img_num], groups=[self.sprite_group, self.tile_group, self.touch_group])
                    # elif img_num == 16:
                    #     num = choices([1, 2, 3, 4, 5, 6, 7])
                    #     num = num[0]
                    #     # num = 7
                    #     if num == 1:
                    #         enemy.EnemyShooter(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group, self.touch_group, self.enemy_group])
                    #     elif num == 2:
                    #         enemy.EnemyWomanWarrior(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group, self.touch_group, self.enemy_group])
                    #     elif num == 3:
                    #         enemy.EnemySkeleton(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group, self.touch_group, self.enemy_group])
                    #     elif num ==4:
                    #         enemy.EnemyElyxStormblade(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group, self.touch_group, self.enemy_group])
                    #     elif num ==5:
                    #         enemy.EnemyZurael(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group, self.touch_group, self.enemy_group])
                    #     elif num ==6:
                    #         enemy.EnemyWhiteWidow(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group, self.touch_group, self.enemy_group])
                    #     elif num ==7:
                    #         enemy.EnemyKheshraiFanblade(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group, self.touch_group, self.enemy_group])
                    # elif img_num == 17:
                    #     ItemBox.ammo_box(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group])
                    # elif img_num == 18:
                    #     ItemBox.grenades_box(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group])
                    # elif img_num == 19:
                    #     ItemBox.health_box(col * self.TILE_SIZE, row * self.TILE_SIZE, groups=[self.sprite_group])


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