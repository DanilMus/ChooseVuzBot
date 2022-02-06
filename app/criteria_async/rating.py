from bs4 import BeautifulSoup
import aiohttp


async def rating_abro(url):
    async with aiohttp.ClientSession() as session:
        src = await session.get(url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        vuz_rating = soup.find_all(class_='panel rating-table__rating')

        for i in range(len(vuz_rating)-1,-1,-1):
            rating_name = vuz_rating[i].find(class_='rating-table__col rating-table__col--main').text
            if 'QS World University Rankings' in rating_name:
                rating_abro = vuz_rating[i].find(class_='rating-table__col rating-table__col--world').text.strip()
                rating_abro = rating_abro.split('-')[0] # бывает, что рейтинг 601-800
                rating_abro = rating_abro.split('+')[0] # или +1001
                rating_abro = int(rating_abro)
                break

        if not(rating_abro):
            rating_abro = 1500

        return rating_abro

async def rating_russ(url):
    async with aiohttp.ClientSession() as session:
        src = await session.get(url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        vuz_rating = soup.find_all(class_='panel rating-table__rating')

        rating_russ = int(vuz_rating[-1].find(class_='rating-table__col rating-table__col--rf').text.strip())

        return rating_russ

