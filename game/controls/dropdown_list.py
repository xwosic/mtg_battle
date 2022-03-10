from typing import Callable, List
from .dropdown_view import DropdownView


class DropdownList:
    """
    Displays list of options and sends choise to target method.
    """
    def __init__(self, game, options_list: List[str], send_choice_to: Callable):
        options = self.prepare_options_dict(options_list)
        self.dropdown_view = self.create_list(game, options)
        self.send_choice_to = send_choice_to

    def prepare_options_dict(self, options_list):
        options = {}
        for option_name in options_list:
            options[option_name] = {'instance': None, 'kwargs': {}}

        return options

    def create_option_function(self, option_name: str):
        def mock():
            # this will send option_name (choice for list) to target callable
            self.send_choice_to(option_name)
        return mock

    def create_list(self, game, options, **kwargs):
        dw = DropdownView.__new__(DropdownView)
        for method, method_dict in options.items():
            method_dict['instance'] = dw
            dw.__setattr__(method, self.create_option_function(method))
        DropdownView.__init__(dw, game=game, options=options, **kwargs)
        dw.dropdown.distribute_buttons(dw.dropdown.buttons,
                                       button_w=200,
                                       button_h=game.screen.height//len(dw.dropdown.buttons))
        return dw
