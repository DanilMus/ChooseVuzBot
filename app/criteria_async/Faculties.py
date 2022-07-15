from bs4 import BeautifulSoup
import aiohttp

def dict_plus_dict(d1: dict, d2: dict):
    d3 = {}
    for key1, val1 in d1.items():
        d3[key1] = val1
    for key2, val2 in d2.items():
        d3[key2] = val2
    return d3

def do_new_url(url, subj):
    new_url = url + '/poege/'
    if "Математика" in subj:
        new_url += 'egemat;'
    if "Русский язык" in subj: 
        new_url += 'egerus;' 
    if "Информатика" in subj:
        new_url += 'egeinform;'
    if "История" in subj:
        new_url += 'egeist;'
    if "Обществознание" in subj:
        new_url += 'egeobsh;'
    if "Иностранный язык" in subj:
        new_url += 'egeinyaz;'
    if "География" in subj:
        new_url += 'egegeorg;'
    if "Физика" in subj:
        new_url += 'egefiz;'
    if "Биология" in subj:
        new_url += 'egebiol;'
    if "Литература" in subj:
        new_url += 'egeliter;'
    if "Химия" in subj:
        new_url += 'egehim;'
    # вступительный, вдруг как в МГУ
    new_url += 'vstup;'
    
    return new_url
    
def find_pagination(soup):
    try: 
        pagination = soup.find(class_='pagination')
    except:
        pass

    if pagination:
        info = pagination.find_all('li')
        for elem in info:
            page = elem.text.strip()
            if page.isdigit():
                pagination = int(page)
    else:
        pagination = 1

    return pagination


# конкретно работает со страницей
async def Faculties_count(url, session):
    async with session.get(url) as src:
        soup = BeautifulSoup(await src.text(), 'lxml')

        faculties = soup.find_all(class_='col-md-12 shadowForItem')
        bal, bud = 0, 0
        faculties_dict = {}

        for faculty in faculties:
            faculty_info = faculty.find_all(class_='col-md-4 itemSpecAllParamWHide newbl')[1]
            elem = faculty_info.find_all(class_='tooltipq')

            if (elem) and (elem[0]) and (elem[2]):
                bal = elem[0].text.replace('минимальный суммарный проходной балл на бюджет по специальности','').strip('от ')
                if (bal) and (bal.isdigit()):
                    bal = int(bal)
                else: 
                    bal = 0

                bud = elem[2].text.replace('количество бюджетных мест на специальность','').strip(' мест')
                if (bud) and (bud.isdigit()):
                    bud = int(bud)
                else: 
                    bud = 0

                faculty_name = faculty.find(class_= 'itemSpecAllinfo').find('div').text.strip()
                
                if (bal) and (bud):
                    faculties_dict[faculty_name] = [bal, bud]
        
        return faculties_dict


# главная функция
async def Faculties(url, subj):
    new_url = do_new_url(url, subj)

    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)

        soup = BeautifulSoup(await src.text(), 'lxml')
        
        # проверка на комбинации с предметами
        subjcombs = [] # какие предметы используются
        try: 
            egecombs = soup.find(class_= 'egecombs')
            egecombs = egecombs.find_all('a')
            for i in range(len(egecombs)):
                subjcomb = egecombs[i].find_all(class_= 'cpPara')
                for j in range(len(subjcomb)):
                    subjcomb[j] = subjcomb[j].text.strip()
                subjcombs.append('_'.join(subjcomb))

                egecombs[i] = 'https://vuzopedia.ru/' + egecombs[i].get('href')

        except Exception:
            egecombs = [new_url] # если нет комбинаций, то просто обычная ссылка
            subjcombs = ['_'.join(subj)]

        faculties = {}

        for i in range(len(egecombs)):
            new_url = egecombs[i]
            subjcomb = subjcombs[i]
            pages = find_pagination(soup)
            # перебор по страницам (если не будет, то просто возмет 1 стр.)
            for i in range(pages):
                part_faculties = await Faculties_count(f'{new_url}?page={i+1}', session)
                if i == 0:
                    faculties[subjcomb] = part_faculties
                else:
                    faculties[subjcomb] = dict_plus_dict(faculties[subjcomb], part_faculties)


        return faculties