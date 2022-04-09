import json
import os 

# как строиться база
# {
#   "Название ВУЗа": [
#       [
#           "сслыка на tabiturient.ru",
#           "сслыка на vuzopedia.ru",
#           "сслыка на ucheba.ru",          
#       ],
#       счетчик, сколько раз данные на этот ВУЗ совпадали,
#       [
#           [баллы ЕГЭ на факультеты],
#           [бюджетные места на факультеты],
#           [баллы на крутые факультеты],
#           [бюджетные места на крутые факультеты],
#           военная кафедра,
#           количество учеников на 1-го учителя,
#           русский рейтинг,
#           зарубежный рейтинг,
#           отзывы,
#           общежитие
#       ]
#   ]
# }



if not(os.path.exists('data')):
    os.mkdir('data')

if not(os.path.exists('data/data.json')):
    with open('data/data.json','w',encoding='utf-8') as file:
        json.dump({}, file, indent= 4, ensure_ascii= False)

class db_worker:
    @staticmethod
    def get_vuz(name):
        with open('data/data.json','r',encoding='utf-8') as file:
            data = json.load(file)
        
        vuz = data.get(name,0)

        return vuz

    @staticmethod
    def get_data():
        with open('data/data.json','r',encoding='utf-8') as file:
            data = json.load(file)
        
        return data

    @staticmethod
    def download_new_vuz(vuz_name: str, vuz_urs: list, vuz_info:list):
        with open('data/data.json','r',encoding='utf-8') as file:
            data = json.load(file)
        
        data[vuz_name] = [vuz_urs, 0, vuz_info]

        with open('data/data.json','w',encoding='utf-8') as file:
            json.dump(data, file, indent= 4, ensure_ascii= False)

    @staticmethod
    def update_count_of_vuz(name:str):
        with open('data/data.json','r',encoding='utf-8') as file:
            data = json.load(file)
        
        data[name] = data[name][1] + 1

        with open('data/data.json','w',encoding='utf-8') as file:
            json.dump(data, file, indent= 4, ensure_ascii= False)