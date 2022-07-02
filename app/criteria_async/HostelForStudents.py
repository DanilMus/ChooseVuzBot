from bs4 import BeautifulSoup
import aiohttp

async def HostelForStudents(url):
    new_url = url + '/obsh'

    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        info = soup.find_all(class_='font2')
        if (info[2].text.strip() == 'В этом вузе есть общежитие'):
            obsh = 1

            if ('Оценка общежития: ' in info[3].text):
                rating = info[3].find('b').text
                rating = rating.split('/')[0]
                rating = float(rating.strip()) / 10
                obsh += rating
            elif ('Оценка общежития: ' in info[4].text):
                rating = info[4].find('b').text
                rating = rating.split('/')[0]
                rating = float(rating.strip()) / 10
                obsh += rating

        else:
            obsh = 0

        return obsh