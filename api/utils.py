import aiohttp


async def get(session: aiohttp.ClientSession, url: str):
    """
    Get a una url
    """
    async with session.get(url) as response:
        return await response.json()
