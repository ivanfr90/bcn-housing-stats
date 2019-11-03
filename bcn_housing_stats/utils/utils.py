import asyncio
import logging

import aiohttp as aiohttp

logger = logging.getLogger(__name__)


async def fetch_all_data(urls: list):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(
                fetch_data(url=url['url'], params=url['params'], session=session, timeout=5))
            tasks.append(task)
        data_list = await asyncio.gather(*tasks, return_exceptions=True)
    return data_list


async def fetch_data(url: str, params: dict, session, timeout):
    try:
        logger.info(f'Fetching data from {url}')
        async with session.get(url, params=params, timeout=timeout) as response:
            logger.info(f'Response status: {response.status}')
            if response.status == 200:
                return await response.json()
    except Exception as e:
        logger.error(f'An error occurred fetching data from {response.url}',
                     exc_info=True, extra={'exception': e})
