from platform import python_branch
import pygame


class Game:
    pass


class Mouse:
    def __call__(self, game: Game, mouse_event: pygame.event.Event):
        if mouse_event.button == 1:
            # left-click
            clicked = [go for go in game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for one in clicked:
                one.left_click()
                break
        
        elif mouse_event.button == 3:
            # right-click
            clicked = [go for go in game.sprite_group.sprites() if go.rect.collidepoint(mouse_event.pos)]
            for one in clicked:
                one.right_click()
                break

