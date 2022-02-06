from bs4 import BeautifulSoup
import aiohttp

async def milit_department(url):
    async with aiohttp.ClientSession() as session:
        src = await session.get(url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        vuz_options = soup.find(class_='vuzOpiton').find_all('i')
    
        if 'vuzok' in vuz_options[2].get('class'):
            return 1
            
        return 0