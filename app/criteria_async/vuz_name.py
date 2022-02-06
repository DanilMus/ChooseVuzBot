from bs4 import BeautifulSoup
import aiohttp

async def vuz_name(url):
    async with aiohttp.ClientSession() as session:
        src = await session.get(url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        vuz = soup.find(class_='choosevuz insertVpm').find('span').text.strip()

        return vuz