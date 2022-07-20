from bs4 import BeautifulSoup
import aiohttp

async def GTO_GoldMedal(url):
    async with aiohttp.ClientSession() as session:
        src = await session.get(url)

        soup = BeautifulSoup(await src.text(), 'lxml')
        
        gto = 0
        gold_medal = 0

        all_info = soup.find_all(class_= 'col-md-6 col-sm-6')

        for info in all_info:
            name = info.find(class_= 'mainTitleBlTelo')

            if (name) and (name.text.strip() == 'Дополнительные баллы к ЕГЭ'):
                add_bals = info.find_all(class_= 'clearfix')

                for add_bal in add_bals:
                    what_is_it = add_bal.find(class_= 'indDostrLeft')

                    if (what_is_it) and (what_is_it.text.strip() == 'За золотой значок ГТО'):
                        gto = add_bal.find(class_= 'progress-bar')
                        gto = gto.text.strip().strip(' балл').strip(' балла').strip(' баллов')
                        if gto.isdigit():
                            gto = int(gto)

                    elif (what_is_it) and (what_is_it.text.strip() == 'За золотую медаль'):
                        gold_medal = add_bal.find(class_= 'progress-bar')
                        gold_medal = gold_medal.text.strip().strip(' балл').strip(' балла').strip(' баллов')
                        if gold_medal.isdigit():
                            gold_medal = int(gold_medal)
                
                return gto, gold_medal
        

