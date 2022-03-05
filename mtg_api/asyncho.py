from typing import List, Union
from pathlib import Path
import aiohttp
import aiofiles
import asyncio
import json


async def get_card_image(card_name: str,
                         path_to_cards: Union[Path, str],
                         default_url: str = 'https://api.magicthegathering.io/v1/cards?name='):

    print(f'downloading |#__| {card_name}')
    response_body = {}
    async with aiohttp.ClientSession() as session:
        async with session.get(default_url + card_name) as response:
            if response.status == 200:
                response_body = await response.text()

    response_body = json.loads(response_body)

    for card in response_body['cards']:
        if card.get('imageUrl'):
            await download_card(url=card['imageUrl'],
                                card_name=card_name,
                                path_to_cards=path_to_cards)
            break


async def get_token_image(token_name: str,
                          path_to_cards: Union[Path, str],
                          query: dict = None,
                          default_url: str = 'https://api.scryfall.com/cards/search'):
    print(f'downloading |#__| {token_name}')
    response_body = {}
    query = await create_query(type='token', **query)
    order = 'order=released'
    print(default_url + '?' + query + '&' + order)
    async with aiohttp.ClientSession() as session:
        async with session.get(default_url + '?' + query + '&' + order) as response:
            if response.status == 200:
                response_body = await response.text()

    response_body = json.loads(response_body)
    image_url = await get_the_most_recent_image_url(response_body)
    await download_card(url=image_url, card_name=token_name, path_to_cards=path_to_cards)


async def get_the_most_recent_image_url(response: dict, size: str = 'small'):
    data = response['data']
    for card in data:
        try:
            url = card['image_uris'][size]
            return url
        except KeyError:
            pass
    raise ValueError(f'There is no image uri for: {response}')


async def create_query(**kwargs):
    query = 'q='
    conditions = [f'{k}%3A{v}' for k, v in kwargs.items()]
    return query + '+'.join(conditions)


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


async def execute_tasks(cards_to_download: List[str], path_to_cards: Union[Path, str], token_queries: dict = None):
    tasks = []
    for card in cards_to_download:
        if token_queries:
            tasks.append(get_token_image(token_name=card, path_to_cards=path_to_cards, query=token_queries[card]))
        else:
            tasks.append(get_card_image(card_name=card, path_to_cards=path_to_cards))

    await asyncio.gather(*tasks)


def download_cards(cards_to_download: List[str], path_to_cards: Path, token_queries: dict = None):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(execute_tasks(cards_to_download, path_to_cards, token_queries=token_queries))

    except Exception as ex:
        print('loop exception:', ex)
        loop.close()
