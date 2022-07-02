from bs4 import BeautifulSoup
import aiohttp

async def VuzUrl(url):
    new_url = url + '/about'

    async with aiohttp.ClientSession() as session:
        src = await session.get(new_url)

        soup = BeautifulSoup(await src.text(), 'lxml')
        
        try:
            vuz_url = soup.find(class_='p40 pm40 obram obramvuz1').find('a').get('href')
        except Exception as ex:
            print(ex)
            print('Скорее всего ссылки на ВУЗ не нашлось на сайте.')
            vuz_url = ''

        return vuz_url