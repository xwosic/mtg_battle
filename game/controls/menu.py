from .dropdown_view import DropdownView
from .dropdown_list import DropdownList
from game.piles.deck import get_deck_filenames
from game.player import Player


class Menu(DropdownView):
    """
    This is parent class of all menu choises.
    After clicking on option, new submenu is created.

    Life total is global for all instances.
    First DropdownList instance sets life total.
    Then next instance of DropdownList chooses deck.
    And after this - player generator is called
    with deck name and health values.
    """
    PLAYERS_LIFE_TOTAL = 20

    def __init__(self, game, **kwargs) -> None:
        self.game = game
        self.new_player = self.player_generator()
        next(self.new_player)
        for _ in range(len(self.game.players)):
            self.new_player.send(('skip', 'this'))

        options = {
            'add_player': {'instance': self, 'kwargs': {}},
            'exit': {'instance': game, 'kwargs': {}}
        }
        super().__init__(game, options, **kwargs)

    def add_player(self):
        options = ['20', '30', '40']
        DropdownList(self.game, options, self.set_life_total)

    def choose_deck(self):
        """
        Get decks names and display them in list.
        """
        decks_names = get_deck_filenames()
        options = []
        for name in decks_names:
            name = str(name)
            path, name = name.split('\\')
            name, suffix = name.split('.')
            name = name.replace(' ', '_')
            options.append(name)
        DropdownList(self.game, options, self.create_player)

    def player_generator(self):
        # first next() is to "warm up" the generator
        game = self.game
        deck_name = 'foo'
        health = 'bar'
        deck_name, health = yield 'ready'
        c = (0, 0, 0)
        x = 0
        y = game.screen.height//2
        w = game.screen.width
        h = game.screen.height//2
        a = 0.0
        while True:
            if deck_name == 'skip' and health == 'this':
                deck_name, health = yield
            else:
                deck_name, health = yield Player(game=game,
                                                 deck=deck_name,
                                                 health=health,
                                                 scale=1,
                                                 c=c,
                                                 x=x,
                                                 y=y,
                                                 w=w,
                                                 h=h,
                                                 a=a)
            c = (255, 0, 0)
            x = game.screen.width
            y = game.screen.height//2
            w = game.screen.width
            h = game.screen.height//2
            a = 180.0

    def create_player(self, players_deck: str):
        if len(self.game.players) <= 1:
            players_deck = players_deck.replace('_', ' ')
            player = self.new_player.send((players_deck, Menu.PLAYERS_LIFE_TOTAL))
            self.game.players.append(player)

    def set_life_total(self, life: str):
        life = int(life)
        Menu.PLAYERS_LIFE_TOTAL = life
        self.choose_deck()
