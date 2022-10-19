from bs4 import BeautifulSoup
import aiohttp

async def AdditionalActivities(url):
    new_url = url + '/about'
    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)
        soup = BeautifulSoup(await src.text(), 'lxml')

        info = soup.find_all(class_='font3')
        if len(info) > 9:
            n = info[8].text.strip()
            if n.replace('.','',1).isdigit():
                return float(n)
        
        return 0
