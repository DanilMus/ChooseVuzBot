from bs4 import BeautifulSoup
import aiohttp

async def PriceOfLunch(url):
    new_url = url + '/about'
    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)
        soup = BeautifulSoup(await src.text(), 'lxml')

        info = soup.find_all(class_='nonmobile')
        for i in range(len(info)):
            elem = info[i]
            elem = elem.text.strip()
            if elem == 'Рублей. Средняя стоимость обеда в столовой':
                return float(info[i-2].text.strip())
        
        return 0

