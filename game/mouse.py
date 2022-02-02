from platform import python_branch
import pygame
from game.game_object import GameObject
from typing import List

class Game:
    pass


class MouseDown:
    def __init__(self, game: Game, mouse_event: pygame.event.Event):
        if mouse_event.button == 1:
            # left-click
            clicked: List[GameObject] = [go for go in game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for on_top in reversed(clicked):
                on_top.left_click(mouse_event=mouse_event)
                break
        
        elif mouse_event.button == 3:
            # right-click
            clicked: List[GameObject] = [go for go in game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for on_top in reversed(clicked):
                on_top.right_click(mouse_event=mouse_event)
                break


class MouseUp:
    def __init__(self, game: Game, mouse_event: pygame.event.Event):
        if mouse_event.button == 1:
            # left-upclick
            clicked: List[GameObject] = [go for go in game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for on_top in reversed(clicked):
                on_top.left_upclick(mouse_event=mouse_event)
                break
        
        elif mouse_event.button == 3:
            # right-upclick
            clicked: List[GameObject] = [go for go in game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for on_top in reversed(clicked):
                on_top.right_upclick(mouse_event=mouse_event)
                break
