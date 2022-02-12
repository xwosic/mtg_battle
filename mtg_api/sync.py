import requests
from mtgsdk import Card
from typing import List, Union
from pathlib import Path


def check_which_card_to_download(card_names: List[str], folder: Union[str, Path]):
    """
    Checks which cards are already downloaded and returns list to download
    """
    if isinstance(folder, str):
        folder = Path(folder)

    if not folder.exists():
        # there are no downloaded cards
        folder.mkdir(parents=True)
        return card_names

    existing_cards = []
    for file in folder.iterdir():
        if file.is_file():
            existing_cards.append(file.stem)

    to_download = []
    for card in card_names:
        if card not in existing_cards:
            to_download.append(card)
    
    return to_download


def download_cards(card_names: List[str], folder: Union[str, Path]):
    """
    Downloads cards into folder
    """

    for name in card_names:
        print(f'downloading |   | {name}', end="")
        result: List[Card] = Card.where(name=name).all()

        for c in result:
            if c.image_url is not None:
                print(f'\rdownloading |#  | {name}', end="")

                image = requests.get(c.image_url).content

                print(f'\rdownloading |## | {name}', end="")

                card_path = Path.joinpath(folder, f"{name}.jpg")

                with open(card_path, 'wb') as file:
                    file.write(image)

                print(f'\rdownloading |###| {name}')
                break  # the most recent version is returned as first
