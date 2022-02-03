from platform import python_branch
import pygame
from game.clickable import Clickable
from game.game_object import GameObject
from typing import List

class Game:
    pass



class Mouse:
    def __init__(self, game: Game):
        self.game = game
        self.left_button_down = False
        self.right_button_down = False

    def mouse_down(self, mouse_event: pygame.event.Event):
        if mouse_event.button == 1:
            # left-click
            self.left_button_down = True
            clicked: List[GameObject] = [go for go in self.game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for on_top in reversed(clicked):
                if isinstance(on_top, Clickable):
                    on_top.left_click(mouse_event=mouse_event)
                    break
        
        elif mouse_event.button == 3:
            # right-click
            self.right_button_down = True
            clicked: List[GameObject] = [go for go in self.game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for on_top in reversed(clicked):
                if isinstance(on_top, Clickable):
                    on_top.right_click(mouse_event=mouse_event)
                    break
    
    def mouse_up(self, mouse_event: pygame.event.Event):
        if mouse_event.button == 1:
            # left-upclick
            self.left_button_down = False
            clicked: List[GameObject] = [go for go in self.game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for on_top in reversed(clicked):
                if isinstance(on_top, Clickable):
                    on_top.left_upclick(mouse_event=mouse_event)
                    break
        
        elif mouse_event.button == 3:
            # right-upclick
            self.right_button_down = False
            clicked: List[GameObject] = [go for go in self.game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for on_top in reversed(clicked):
                if isinstance(on_top, Clickable):
                    on_top.right_upclick(mouse_event=mouse_event)
                    break
