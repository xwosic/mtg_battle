from game.clickable import Clickable


class Dragable(Clickable):
    """
    Class inheriting after Dragable has drag and drop functionality.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drag = False
        self.loc = None
        self.mouse_offset = (0, 0)

    # def left_click(self, mouse_event: pygame.event.Event, **kwargs):
    #     """
    #     Dragging starts after mouse's left button is clicked.
    #     """
    #     self.drag = True

    #     # add to top when drag
    #     self.game.sprite_group.remove(self)
    #     self.game.sprite_group.add(self)

    #     if self.loc:
    #         self.loc.remove_card(self)
    #         self.loc = None
    #     self.mouse_offset = (mouse_event.pos[0] - self.rect.x, mouse_event.pos[1] - self.rect.y)
    #     return super().left_click(mouse_event, **kwargs)

    # def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
    #     """
    #     Object is dropped when mouse's left button is reliesed.
    #     """
    #     self.drag = False
    #     self.drop_to_zone(mouse_event.pos)
    #     return super().left_upclick(mouse_event, **kwargs)

    # def update(self) -> None:
    #     """
    #     If mouse's left button is pressed and mouse is moving, object will follow.
    #     """
    #     if self.drag:
    #         self.rect.x = pygame.mouse.get_pos()[0] - self.mouse_offset[0]
    #         self.rect.y = pygame.mouse.get_pos()[1] - self.mouse_offset[1]

    #     return super().update()

    def drop_into(self, pos):
        for player in self.game.players:
            for zone in player.zones:
                if zone.is_clicked(pos):
                    self.loc.remove_card(self)
                    self.loc = None
                    zone.add_card(self)
                    break
