import pygame
from game.clickable import Clickable
from game.dragable import Dragable


class Game:
    pass


class Mouse:
    def __init__(self, game: Game):
        self.game = game
        self.left_button_down = False
        self.right_button_down = False
        self.dragged_object = None
        self.start_pos = None
        self.end_pos = None
        self.mouse_offset = (0, 0)

    def get_clicked(self, mouse_event: pygame.event.Event):
        """
        Get clicked object which was on top of clicked objects.
        """
        clicked = [g_obj for g_obj in self.game.sprite_group.sprites() if g_obj.rect.collidepoint(mouse_event.pos)]
        clicked_object = None
        for on_top in reversed(clicked):
            if isinstance(on_top, Clickable):
                clicked_object = on_top
                break

        print(clicked_object)
        return clicked_object

    def is_moved(self):
        """
        Returns true if between click and upclick position was changed."""
        return self.start_pos != self.end_pos

    def mouse_down(self, mouse_event: pygame.event.Event):
        clicked = self.get_clicked(mouse_event=mouse_event)
        self.start_pos = mouse_event.pos
        # left-click
        if mouse_event.button == 1:
            self.left_button_down = True
            if isinstance(clicked, Dragable):
                self.dragged_object = clicked
                self.mouse_offset = (mouse_event.pos[0] - self.dragged_object.rect.x,
                                     mouse_event.pos[1] - self.dragged_object.rect.y)

        # right-click
        elif mouse_event.button == 3:
            self.right_button_down = True

    def mouse_up(self, mouse_event: pygame.event.Event):
        clicked = self.get_clicked(mouse_event=mouse_event)
        self.end_pos = mouse_event.pos
        # left-upclick
        if mouse_event.button == 1:
            # check if mouse moved - tap
            if self.is_moved():
                print('moved')
                # drop
                if clicked == self.dragged_object:
                    if self.dragged_object:
                        self.dragged_object.drop_into(self.end_pos)
            else:
                print('not moved')
                # click
                if clicked:
                    if 'left_upclicked_trigger' in clicked.__dict__:
                        print('trigger')
                        clicked.left_upclicked_trigger()
                    else:
                        print('upclick')
                        clicked.left_upclick(mouse_event=mouse_event)

            
            self.left_button_down = False
            self.dragged_object = None

        elif mouse_event.button == 3:
            # right-upclick
            self.right_button_down = False

    def update(self):
        if self.dragged_object:
            self.dragged_object.rect.x = pygame.mouse.get_pos()[0] - self.mouse_offset[0]
            self.dragged_object.rect.y = pygame.mouse.get_pos()[1] - self.mouse_offset[1]
