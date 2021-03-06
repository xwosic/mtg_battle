from .dropdown import Dropdown
from .fog import Fog


class DropdownView:
    def __init__(self, game, options, **kwargs) -> None:
        self.fog = Fog.full_screen_fog(game=game)
        self.dropdown = Dropdown(game=game, options=options, **kwargs)
        self.fog.victims.append(self.dropdown)
        self.dropdown.victims.append(self.fog)
