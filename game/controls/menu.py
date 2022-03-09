from .dropdown_view import DropdownView


class Menu(DropdownView):
    def __init__(self, game, **kwargs) -> None:
        options = {
            'exit': {'instance': game, 'kwargs': {}}
        }
        super().__init__(game, options, **kwargs)
