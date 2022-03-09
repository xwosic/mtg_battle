from .dropdown_view import DropdownView
from game.piles.deck import get_deck_filenames


class Menu(DropdownView):
    def __init__(self, game, **kwargs) -> None:
        self.game = game
        options = {
            'new': {'instance': self, 'kwargs': {}},
            'exit': {'instance': game, 'kwargs': {}}
        }
        super().__init__(game, options, **kwargs)

    def new(self):
        """
        Create new game:
            * choose decks
            * choose amount of life
        """
        decks_names = get_deck_filenames()
        options = {}
        for name in decks_names:
            name = str(name)
            name = name.lstrip('decks\\')
            name = name.rstrip('.txt')
            name = name.replace(' ', '_')
            options[name] = {'instance': None, 'kwargs': {}}
        print(options)
        self.submenu(self.game, options)

    def submenu(self, game, options, **kwargs):
        new_object = DropdownView.__new__(DropdownView)
        for method, method_dict in options.items():
            method_dict['instance'] = new_object

            def mock():
                print(method)

            new_object.__setattr__(method, mock)

        return DropdownView.__init__(new_object, game=game, options=options, **kwargs)
