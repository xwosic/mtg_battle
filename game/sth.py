import pygame
from game.loader import scrapp_images, get_animations_from_sprite_sheet


# important!
# calling method on higher class level causes conflicts with overwritten class attributes!


class Sth(pygame.sprite.Sprite):
    """Sth is everything. This is base class for every sprite object in game."""
    # animation actions must be loaded before any instance can be created
    animation_actions = {}
    # health on start
    max_health = 100
    # how quickly animation frames changes
    animation_cooldown = 100
    # game scale - every scallable thing should be multiplied by this
    game_scale = 0.75

    def __init__(self, x, y, groups=None, start_animation='idle', rect_width=None, rect_height=None, **kwargs):
        """rect_width - collidable width of rect, rect_height (animation can be bigger than rect) - collidable height of rect (animation can be bigger than rect)"""
        pygame.sprite.Sprite.__init__(self)
        # animation
        self.animation_rect_x_offset = 0
        self.animation_rect_y_offset = 0
        if self.animation_actions:
            self.animation_action_name = start_animation
            self.animation_list = self.animation_actions[self.animation_action_name][self.animation_action_name]
            self.animation_index = 0
            self.animation_index_limit = len(self.animation_list) - 1
            self.last_update_time = pygame.time.get_ticks()
            self.animation_action_style = 'loop'
            self.image = self.animation_list[self.animation_index]
            self.rect = pygame.Rect(x, y, 0, 0)
            
            # set rect size if animation frame is too big to be usefull as rect size
            if rect_width:
                self.rect.width = rect_width
                self.animation_rect_x_offset = rect_width // 2 - self.image.get_width() // 2
            
            else:
                self.rect.width = self.image.get_width()

            if rect_height:
                self.rect.height = rect_height
                self.animation_rect_y_offset = rect_height // 2 - self.image.get_height() // 2
            
            else:
                self.rect.height = self.image.get_height()

            self.rect.center = (x, y)

            # animations added to queue will be performed after current animation ends
            self.animation_queue = []
            # animation frame can be marked as event (to trigger things)
            self.animation_frame_event_numbers = []
            self.animation_frame_event = False
        
        else:
            self.image = pygame.Surface((x, y))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        self.flip = False        
        # position and movement
        
        self.direction = 1
        self.dx = 0
        self.dy = 0
        self.vel_x = 0
        self.vel_y = 0
        # entity variables
        self.alive = True
        self.health = self.max_health
        self.in_air = False
        self.states = {}
        # universal setter
        self.universal_setter(**kwargs)
        # add to sprite group at the moment of creation
        if groups != None:
            # list of groups to add new sprite
            for group in groups:
                group.add(self)

    def universal_setter(self, **kwargs):
        """
        This method enables to make modifications (set or overwrite) in Sth attributes from inheriting class level.
        Just pass attribute name you want to modify and value as **kwargs.
        For example:
            if you want to generate not alive object (every Sth object is created alive by default)
            obj = ClassName(x, y, alive=False)
        """
        for attr_name in kwargs:
            self.__dict__[attr_name] = kwargs[attr_name]

    @classmethod
    def load_animations(cls, path_to_images, scale=1, perform_style={'death': 'once'}):
        """
        Loading animations should be called on very beginning of the game or at least before first instance of class is created.
        """
        cls.animation_actions = scrapp_images(path_to_images, scale=scale)
        cls.set_animation_perform_style(perform_style)

    @classmethod
    def load_animations_from_sprite_sheet(cls, path_to_spritesheet, actions_dict, perform_style={'jump': 'once', 'death': 'once'}, start_point=(0,0), scale=1, left_marigin=0, right_marigin=0, top_marigin=0, bottom_marigin=0, frame_width=0, frame_height=0):
        """
        path_to_spritesheet - 'path to image with sprite sheet',
        actions_dict - {'animation_name':num_of_frames_in_animation},
        frame_width - width of rectangle created from this sprite sheet's frame,
        frame_height - height of rectangle created from this sprite sheet's frame, 
        start_point - modify this to for example set character in the center of rectangle,
        marigin - offset to the left/right/top/bottom of the spritesheet's images,
        returns: dict of structure "animation name": [list, of, images]
        """
        cls.animation_actions = get_animations_from_sprite_sheet(path_to_spritesheet, actions_dict, scale=scale, start_point=start_point, left_marigin=left_marigin, right_marigin=right_marigin, frame_width=frame_width, top_marigin=top_marigin, bottom_marigin=bottom_marigin, frame_height=frame_height)
        cls.set_animation_perform_style(perform_style)

    @classmethod
    def set_animation_perform_style(cls, animation_styles: dict):
        """
        input: {
                'idle': 'perform_style': 'loop',
                'attack_1': 'perform_style': 'once__1'
                'spinning': 'perform_style': 'loop__3'
            }

        output: {
            'idle': {
                'perform_style': 'loop',
                'event_on_frame': None,
                'idle': list_of_frames
                },
            'attack_1': {
                'perform_style': 'once', 
                'event_on_frame': 1, 
                'attack_1': list_of_frames
                },
            }
        """

        for animation_name, animation_list in cls.animation_actions.items():
            if animation_name in animation_styles:
                name_of_style = animation_styles[animation_name]
                number_of_event_frames = []
                if '__' in name_of_style:
                    # loop__3 or attack_2__1__7 (attack number 2 with actions on 1'st and 7'th frame)
                    name_of_style, *number_of_event_frames = name_of_style.split('__')

                cls.animation_actions[animation_name]={
                    "perform_style": name_of_style,
                    animation_name: animation_list,
                    "event_on_frame": number_of_event_frames
                    }

            else:
                cls.animation_actions[animation_name]={
                    "perform_style": 'loop',
                    animation_name: animation_list,
                    "event_on_frame": []
                    }

    @classmethod
    def overwrite_animation_action(cls, source_animation_name, source_animation_list_indexes, target_animation_name):
        start_index, stop_index = source_animation_list_indexes
        cls.animation_actions[target_animation_name][target_animation_name] = cls.animation_actions[source_animation_name][source_animation_name][start_index : stop_index]
    
    def get_hit(self, demage, game):
        self.health -= demage
        if self.health < 0 :
            self.health = 0

        if self.health == 0:
            self.death_time = pygame.time.get_ticks()
            if self.alive:
                self.animation_queue.clear()
                self.change_animation_action('death', reset_index=True)
                # Blood(self.rect.x, self.rect.y, groups=[game.sprite_group], start_animation='blood')
            self.alive = False

    def change_animation_action(self, new_action_name, reset_index=False):
        if self.animation_action_name != new_action_name:
            self.animation_action_name = new_action_name
            # assigning animation list
            self.animation_list = self.__class__.animation_actions[new_action_name][new_action_name]
            # setting new limit
            self.animation_index_limit = len(self.animation_list) - 1
            # setting style of animation
            self.animation_action_style = self.__class__.animation_actions[new_action_name]['perform_style']
            # setting event frame
            self.animation_frame_event = None
            self.animation_frame_event_numbers = []
            for action_on_frame in self.__class__.animation_actions[new_action_name]['event_on_frame']:
                try:
                    self.animation_frame_event_numbers.append(int(action_on_frame))
                except:
                    pass

        # reseting index
        if reset_index:
            self.animation_index = 0

    def is_event_triggered(self, game):
        if self.animation_frame_event:
            self.triggered_func(game)
            self.animation_frame_event = None

    def triggered_func(self, game):
        pass

    def update_animation(self, states):
        """Changes displayed frame of animation. If animation list contains only one frame, skips changing frame."""          
        # loop animations
        if self.animation_action_style == 'loop':
            if len(self.animation_list) > 1: 
                if pygame.time.get_ticks() - self.last_update_time > self.animation_cooldown:
                    if self.animation_index >= self.animation_index_limit:
                        self.animation_index = 0
                        if self.animation_index in self.animation_frame_event_numbers:
                            self.animation_frame_event = self.animation_action_name

                        else:
                            self.animation_frame_event = None

                        if self.animation_queue:
                            self.change_animation_action(self.animation_queue.pop(0), reset_index=True)
                    
                    else:
                        self.animation_index += 1
                        if self.animation_index in self.animation_frame_event_numbers:
                            self.animation_frame_event = self.animation_action_name

                        else:
                            self.animation_frame_event = None
                        
                    
                    self.image = self.animation_list[self.animation_index]
                    
                    self.last_update_time = pygame.time.get_ticks()
            else:
                self.image = self.animation_list[0]
        
        # one perform animations
        elif self.animation_action_style == 'once':
            # iterates through all frames only once and stays on last frame
            if pygame.time.get_ticks() - self.last_update_time > self.animation_cooldown:
                if self.animation_index <= self.animation_index_limit:
                    self.image = self.animation_list[self.animation_index]
                    if self.animation_index in self.animation_frame_event_numbers:
                            self.animation_frame_event = self.animation_action_name

                    else:
                        self.animation_frame_event = None

                    self.animation_index += 1
                    self.last_update_time = pygame.time.get_ticks()
                
                else:
                    if self.animation_queue:
                            self.change_animation_action(self.animation_queue.pop(0), reset_index=True)                

    def move(self, game):
        # reset on start
        self.dx = 0
        self.dy = 0
        # self movement (ai)
        self.self_movement(game)
        # gravity
        self.add_gravity(game)
        # relative movement to player
        self.move_rel_to_player(game)
        # calculate x and y speed and change position of rect
        self.add_vel_to_position()

    def self_movement(self, game):
        pass

    def add_gravity(self, game):
        """
        Modifies self.vel_y by adding to it gravity speed.
        """
        if self.in_air:
            self.vel_y += game.GRAVITY
        
        else:
            self.vel_y = 0

    def move_rel_to_player(self, game):
        self.dx -= game.player.dx
        self.dy -= game.player.dy

    def add_vel_to_position(self):
        self.dx += self.vel_x
        self.dy += self.vel_y
        self.rect.x += self.dx
        self.rect.y += self.dy          

    # before super().update() addons
    def collide_with_tiles(self, game):
        self.in_air = True
        possible_tiles = pygame.sprite.spritecollide(self, game.tile_group, False)
        for tile in possible_tiles:
            tile_is_on_right = None
            tile_is_under = None
            delta_x = self.rect.centerx - tile.rect.centerx
            delta_y = self.rect.centery - tile.rect.centery
            abs_delta_x = abs(delta_x)
            abs_delta_y = abs(delta_y)

            if abs_delta_x <= abs_delta_y:
                if delta_y > 0:
                    tile_is_under = False

                else:
                    tile_is_under = True
            else:
                if delta_x > 0:
                    tile_is_on_right = False

                else:
                    tile_is_on_right = True

            self.do_on_tile_collision(tile, tile_is_under, tile_is_on_right)

    def do_on_tile_collision(self, tile, tile_is_under, tile_is_on_right):
            if tile_is_under != None:
                if tile_is_under:
                    self.tile_is_under_collision(tile)

                else:
                    self.tile_on_top_collision(tile)

            if tile_is_on_right != None:
                if tile_is_on_right:
                    self.tile_on_right_collision(tile)

                else:
                    self.tile_on_left_collision(tile)                    

    def tile_is_under_collision(self, tile):
        self.rect.bottom = tile.rect.top + 1
        self.in_air = False

    def tile_on_top_collision(self, tile):
        self.rect.top = tile.rect.bottom + 1
        self.in_air = True
        self.vel_y = 0

    def tile_on_right_collision(self, tile):
        self.rect.right = tile.rect.left - 1
        self.vel_x = - self.vel_x

    def tile_on_left_collision(self, tile):
        self.rect.left = tile.rect.right + 1
        self.vel_x = - self.vel_x

    def is_in_window(self, game):
        return game.screen.get_rect().contains(self.rect)

    def kill_outside_window(self, game):
        if not self.is_in_window(game):
            self.kill()
    
    def check_collisions(self, game):
        pass

    def update(self, game):
        self.update_animation(game.states)
        self.is_event_triggered(game)
        self.move(game)
        # clean up dead sprites after 10 sec
        if not self.alive:
            if pygame.time.get_ticks() - self.death_time > 10000:
                self.kill()
        # takes image and bools for flipping in x and y axis
        # pygame.transform.flip(self.image, self.flip, False)
        game.screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x + self.animation_rect_x_offset, self.rect.y + self.animation_rect_y_offset))
        # draw rect around everything
        pygame.draw.rect(game.screen, (0, 255, 0), self.rect, width=1)
