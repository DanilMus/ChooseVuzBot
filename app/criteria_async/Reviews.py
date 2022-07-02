from bs4 import BeautifulSoup
import aiohttp

async def Reviews(url):
    async with aiohttp.ClientSession() as session:
        src = await session.get(url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        reviews = soup.find_all(class_='p10cif')
        
        grade = 0
        if reviews:
            bad = float(reviews[2].find(class_='font11').text.replace('%','').strip())
            middle = float(reviews[1].find(class_='font11').text.replace('%','').strip())
            good = float(reviews[0].find(class_='font11').text.replace('%','').strip())

            grade = (10*good + 5*middle + bad*1) / 100

        return round(grade,2)