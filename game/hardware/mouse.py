import pygame
from game.game_objects import Clickable, Dragable


class Game:
    pass


class Mouse:
    def __init__(self, game: Game):
        """
        In game there is only one Mouse object which handles
        mouse events. It can click Clickable or drag and drop Dragable.
        """
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

        return clicked_object

    def is_moved(self):
        """
        Returns true if between click and upclick position was changed.
        """
        return self.start_pos != self.end_pos

    def move_dragged_on_top(self):
        """
        When object is dragged it is drawn last - always above other objects.
        """
        self.game.sprite_group.remove(self.dragged_object)
        self.game.sprite_group.add(self.dragged_object)

    def mouse_down_left_button(self, mouse_event: pygame.event.Event, clicked):
        """
        When mouse left button is clicked, check if object is dragable.
        If so, add it to dragged and save position.
        """
        if isinstance(clicked, Dragable):
            self.dragged_object = clicked
            self.move_dragged_on_top()
            self.mouse_offset = (mouse_event.pos[0] - self.dragged_object.rect.x,
                                 mouse_event.pos[1] - self.dragged_object.rect.y)

    def mouse_down_right_button(self, mouse_event: pygame.event.Event, clicked):
        """
        On mouse right button set flag.
        """
        self.right_button_down = True

    def mouse_down(self, mouse_event: pygame.event.Event):
        """
        Get clicked object and position. Decide which button was pressed.
        """
        clicked = self.get_clicked(mouse_event=mouse_event)
        self.start_pos = mouse_event.pos
        if mouse_event.button == 1:
            self.mouse_down_left_button(mouse_event, clicked)

        elif mouse_event.button == 3:
            self.mouse_down_right_button(mouse_event, clicked)

    def mouse_up_left_button(self, mouse_event: pygame.event.Event, clicked):
        """
        If mouse hasn't moved since down click - object is clicked.
        Else object was dragged and will be dropped here.
        """
        if self.is_moved():
            # drop
            if clicked == self.dragged_object:
                if self.dragged_object:
                    self.dragged_object.drop_into(self.end_pos)

        else:
            # click
            if clicked:
                clicked.left_upclick(mouse_event=mouse_event)

        self.left_button_down = False
        self.dragged_object = None

    def mouse_up_right_button(self, mouse_event: pygame.event.Event, clicked):
        """
        Right now - nothing happens.
        """
        clicked = self.get_clicked(mouse_event=mouse_event)
        if clicked:
            clicked.right_upclick(mouse_event=mouse_event)

        self.right_button_down = False

    def mouse_up(self, mouse_event: pygame.event.Event):
        """
        Get upclicked and position. Decide which button was upclicked.
        """
        clicked = self.get_clicked(mouse_event=mouse_event)
        self.end_pos = mouse_event.pos
        # left-upclick
        if mouse_event.button == 1:
            self.mouse_up_left_button(mouse_event, clicked)

        elif mouse_event.button == 3:
            # right-upclick
            self.mouse_up_right_button(mouse_event, clicked)

    def update(self):
        """
        When object is dragged, it should have the same position as mouse.
        Offset is a distance between place where mouse is touching the object
        and it's center.
        """
        if self.dragged_object:
            self.dragged_object.rect.x = pygame.mouse.get_pos()[0] - self.mouse_offset[0]
            self.dragged_object.rect.y = pygame.mouse.get_pos()[1] - self.mouse_offset[1]
