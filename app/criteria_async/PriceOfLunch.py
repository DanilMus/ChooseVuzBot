from bs4 import BeautifulSoup
import aiohttp

async def PriceOfLunch(url):
    new_url = url + '/about'
    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)
        soup = BeautifulSoup(await src.text(), 'lxml')

        info = soup.find_all(class_='font4')
        if len(info) > 9:
            n = info[3].text.strip()
            if n.replace('.','',1).isdigit():
                return float(n)

        return 0
