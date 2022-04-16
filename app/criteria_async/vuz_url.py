from bs4 import BeautifulSoup
import aiohttp

async def vuz_url(url):
    new_url = url + '/about'

    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        vuz_url = soup.find(class_='p40 pm40 obram obramvuz1').find('a').get('href')

        return vuz_url