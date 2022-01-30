from typing import List, Union
from pathlib import Path
from mtgsdk import Card
import aiohttp
import aiofiles
import asyncio


async def get_card_image(card_name: str,
                         path_to_cards: Union[Path, str]):

    print(f'downloading |#__| {card_name}')
    result: List[Card] = Card.where(name=card_name).all()
    for c in result:
        if c.image_url is not None:
            await download_card(url=c.image_url,
                                card_name=card_name,
                                path_to_cards=path_to_cards)
            break

async def download_card(url: str, 
                        card_name: str, 
                        path_to_cards: Union[Path, str]):

    print(f'downloading |##_| {card_name}')

    if isinstance(path_to_cards, str):
        path_to_cards = Path(path_to_cards)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                path_to_card = Path.joinpath(path_to_cards, f"{card_name}.jpg")
                f = await aiofiles.open(path_to_card, mode='wb')
                await f.write(await response.read())
                print(f'downloading |###| {card_name}')
                await f.close()


async def download_cards(cards_to_download: List[str], path_to_cards: Union[Path, str]):
    tasks = []
    for card in cards_to_download:
        tasks.append(get_card_image(card_name=card,
                                    path_to_cards=path_to_cards))
    
    await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(download_cards(['Cloudkin Seer', 'Diamond Mare', 'Howling Golem'],
                                            'cards'))

except Exception:
    loop.close()