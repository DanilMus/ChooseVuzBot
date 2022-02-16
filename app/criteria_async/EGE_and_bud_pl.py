from bs4 import BeautifulSoup
import aiohttp

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
    if "Иностранные языки" in subj:
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
            if elem.text.isdigit():
                pagination = int(elem.text)
    else:
        pagination = 1

    return pagination

def do__of_3max(max_bals, buds_for_max_bals):
    count = len([elem for elem in max_bals if elem != 0])
    if count != 0:
        bals_of_3max = sum(max_bals) // count
    else: 
        bals_of_3max = 0
    bud_pl_of_3max = sum(buds_for_max_bals)

    return bals_of_3max, bud_pl_of_3max

def count__of_3max(max_bals, buds_for_max_bals, max_bals_new, buds_for_max_bals_new):
    for i in range(3):
        for j in range(len(max_bals_new)):
            if max_bals[i] < max_bals_new[j]:
                max_bals[i] = max_bals_new[j]
                buds_for_max_bals[i] = buds_for_max_bals_new[j]
                max_bals_new.pop(j)
                buds_for_max_bals_new.pop(j)
                break
    return max_bals, buds_for_max_bals




async def EGE_and_bud_pl_count(url, session):
    async with session.get(url) as src:
        soup = BeautifulSoup(await src.text(), 'lxml')

        info = soup.find_all(class_='col-md-4 itemSpecAllParamWHide newbl')

        bals, buds, count = 0, 0, 0
        max_bals = [0, 0, 0]
        buds_for_max_bals = [0, 0, 0]

        for elems in info[1::3]:
            elem = elems.find_all(class_='tooltipq')

            if (elem) and (elem[0]):
                bal = elem[0].text.replace('минимальный суммарный проходной балл на бюджет по специальности','').strip('от ')
                if (bal) and (bal.isdigit()):
                    bal = int(bal)
                    bals += bal
                    count += 1
                    if bal > max_bals[0]:
                        max_bals[0] = bal
                    elif bal > max_bals[1]:
                        max_bals[1] = bal
                    elif bal > max_bals[2]:
                        max_bals[2] = bal

            if (elem) and (elem[2]):
                bud = elem[2].text.replace('количество бюджетных мест на специальность','').strip(' мест')
                if (bud) and (bud.isdigit()):
                    bud = int(bud)
                    buds += bud
                    if bal == max_bals[0]:
                        buds_for_max_bals[0] = bud
                    elif bal == max_bals[1]:
                        buds_for_max_bals[1] = bud
                    elif bal == max_bals[2]:
                        buds_for_max_bals[2] = bud
        
        if count != 0:
            bals //= count
        else:
            bals = 0
        return bals, buds, max_bals, buds_for_max_bals


async def EGE_and_bud_pl(url, subj):
    new_url = do_new_url(url, subj)

    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)

        soup = BeautifulSoup(await src.text(), 'lxml')

        # проверка на комбинации с предметами
        try: 
            egecombs = soup.find(class_='egecombs')
            egecombs = egecombs.find_all('a')
            for i in range(len(egecombs)):
                egecombs[i] = 'https://vuzopedia.ru/' + egecombs[i].get('href')
        except Exception:
            egecombs = [new_url] # если нет комбинаций, то просто обычная ссылка

        bals, buds, bals_of_3max, bud_pl_of_3max, count = 0, 0, 0, 0, 0
        max_bals = [0, 0, 0]
        buds_for_max_bals = [0, 0, 0]
        # перебор по возможным комбинациям
        for new_url in egecombs:
            pages = find_pagination(soup)
            # перебор по страницам (если не будет, то просто возмет 1 стр.)
            for i in range(pages):
                h1, h2, h3, h4 = await EGE_and_bud_pl_count(f'{new_url}?page={i+1}', session)
                bals += h1
                buds += h2
                max_bals, buds_for_max_bals = count__of_3max(max_bals, buds_for_max_bals, h3, h4)
                count += 1
        
        if count != 0:
            bals //= count
        else:
            bals = 0
        bals_of_3max, bud_pl_of_3max = do__of_3max(max_bals, buds_for_max_bals)
        return bals, buds, bals_of_3max, bud_pl_of_3max