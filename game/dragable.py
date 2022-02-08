from game.clickable import Clickable


class Dragable(Clickable):
    """
    Class inheriting after Dragable has drag and drop functionality.
    Draggable object has to remember where was it's location to
    perform clean leave of previous group.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loc = None

    def drop_into(self, pos):
        """
        This is a trigger to drop action.
        All players' zones are checked and object is assigned to
        the first matching and removed from previous one.
        """
        for player in self.game.players:
            for zone in player.zones:
                if zone.is_clicked(pos):
                    self.loc.remove_card(self)
                    self.loc = None
                    zone.add_card(self)
                    break
