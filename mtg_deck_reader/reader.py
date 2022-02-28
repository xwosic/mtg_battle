from pathlib import Path
from typing import Union


class DeckReader:
    def __init__(self, path: Union[Path, str]):
        if isinstance(path, str):
            path = Path(path)
        self.path = path
        self.cards = {
            'mainboard': {},
            'sideboard': {},
            'commander': {},
            'tokens': {}
        }
        self.destination = 'mainboard'

    def skip_empty(self, line: str):
        return line.startswith('\n')

    def check_destination(self, line: str):
        line = line.strip()
        line = line.strip('\n')
        if line in self.cards.keys():
            self.destination = line
            return True
        return False

    def add_card(self, line: str):
        number, *name = line.split(' ')
        name = ' '.join(name).strip('\n')
        name = name.strip()
        self.cards[self.destination][name] = int(number)
        return f'{name} added to deck in quantity: {number}'

    def check_line(self, file_line: str):
        line = file_line.lower()
        if self.skip_empty(line):
            return 'skipping empty line'
        if self.check_destination(line):
            return f'destination changed to {self.destination}'
        return self.add_card(file_line)

    def read_deck(self) -> dict:
        with open(self.path, 'r') as deck:
            for line in deck:
                print(self.check_line(line))

        return self.cards
