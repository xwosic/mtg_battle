from .dropdown_view import DropdownView
from .dropdown_list import DropdownList
from game.piles.deck import get_deck_filenames
from game.player import Player


class Menu(DropdownView):
    """
    This is parent class of all menu choises.
    After clicking on option, new submenu is created.
    """
    def __init__(self, game, **kwargs) -> None:
        self.game = game
        self.new_player = self.player_generator()
        next(self.new_player)
        for _ in range(len(self.game.players)):
            self.new_player.send(('skip', 'this'))

        options = {
            'new': {'instance': self, 'kwargs': {}},
            'exit': {'instance': game, 'kwargs': {}}
        }
        super().__init__(game, options, **kwargs)

    def new(self):
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
        c = (0, 0, 0)
        x = 0
        y = game.screen.height//2
        w = game.screen.width
        h = game.screen.height//2
        a = 0.0
        deck_name, health = yield 'ready'
        while True:
            print('creating first player')
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
            print('creating second player')
            c = (255, 0, 0)
            x = game.screen.width
            y = game.screen.height//2
            w = game.screen.width
            h = game.screen.height//2
            a = 180.0

    def create_player(self, players_deck: str):
        players_deck = players_deck.replace('_', ' ')
        player = self.new_player.send((players_deck, 20))
        print(player)
        self.game.players.append(player)

