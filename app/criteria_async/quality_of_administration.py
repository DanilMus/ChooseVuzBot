from bs4 import BeautifulSoup
import aiohttp

async def qulity_of_administration(url):
    new_url = url + '/about'
    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)
        soup = BeautifulSoup(await src.text(), 'lxml')

        info = soup.find_all(class_='font2')
        for i in range(len(info)):
            elem = info[i]
            elem = elem.text.strip()
            if elem == 'Качество работы административного аппарата':
                return float(info[i-4].text.strip())
        
        return 0