from bs4 import BeautifulSoup
import aiohttp

async def stud_to_teach_uche(url):
    async with aiohttp.ClientSession() as session:
        src = await session.get(url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        vuz_options = soup.find_all(class_='col-xs-12 col-md-4 key-indicators__item')

        for opt in vuz_options:
            name_opt = opt.find(class_='key-indicators__prop').text.strip()
            if name_opt == 'Преподавателейна 100 студентов':
                stud_to_teach = float(opt.find(class_='key-indicators__val').text.strip()) 
                stud_to_teach = round(100 / stud_to_teach, 2)
                break

        return stud_to_teach

async def stud_to_teach_vuzo(url):
    async with aiohttp.ClientSession() as session:
        src = await session.get(url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        stud_and_teac = soup.find_all(class_='col-md-6 col-sm-6 col-xs-6')
        if stud_and_teac:
            students = int(stud_and_teac[4].text.strip('\nСтудентов '))
            teachers = int(stud_and_teac[6].text.strip('\nПреподавателей '))

            stud_to_teach = round(students / teachers, 2)
        else:
            stud_to_teach = 0

        return stud_to_teach
