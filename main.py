from telnetlib import GA
from mtg_api import check_which_card_to_download, download_cards
from mtg_deck_reader import read_deck
from pathlib import Path
from game.game import Game

def main():
    path = Path('cards')
    deck_path = Path('decks/Reap the Tides.txt')
    deck = read_deck(deck_path)
    deck = list(deck['mainboard'].keys())
    cards_to_download = check_which_card_to_download(deck, path)
    download_cards(cards_to_download, path)

    game = Game()
    game.execute()


if __name__ == '__main__':
    main()
