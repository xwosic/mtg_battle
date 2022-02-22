from pathlib import Path
from typing import Union


def read_deck(path: Union[Path, str]) -> dict:
    if isinstance(path, str):
        path = Path(path)

    cards = {
        'mainboard': {},
        'sideboard': {}
    }

    with open(path, 'r') as deck:
        destination = 'mainboard'
        for card in deck:
            if card.startswith('\n'):
                destination = 'sideboard'
                continue

            number, *name = card.split(' ')
            name = ' '.join(name).strip('\n')
            name = name.strip()
            cards[destination][name] = int(number)

    return cards
