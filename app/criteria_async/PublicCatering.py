from bs4 import BeautifulSoup
import aiohttp

async def PublicCatering(url):
    new_url = url + '/about'
    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)
        soup = BeautifulSoup(await src.text(), 'lxml')

        info = soup.find_all(class_='font2')
        for i in range(len(info)):
            elem = info[i]
            elem = elem.text.strip()
            if elem == 'Качество общепита':
                return float(info[i-2].text.strip())
        
        return 0