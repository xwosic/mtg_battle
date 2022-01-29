from mtg_api import check_which_card_to_download, download_cards
from mtg_deck_reader import read_deck
from pathlib import Path


def main():
    path = Path('cards')
    deck_path = Path('decks/Lorehold Legacies.txt')
    deck = read_deck(deck_path)
    deck = list(deck['mainboard'].keys())
    cards_to_download = check_which_card_to_download(deck, path)
    download_cards(cards_to_download, path)


if __name__ == '__main__':
    main()