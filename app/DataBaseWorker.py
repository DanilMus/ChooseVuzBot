import json
import os   

if not(os.path.exists('data')):
    os.mkdir('data')

if not(os.path.exists('data/data.json')):
    with open('data/data.json', 'w', encoding= 'utf-8') as file:
        json.dump({}, file, indent= 4, ensure_ascii= False)

if not(os.path.exists('data/users.json')):
    with open('data/users.json', 'w', encoding= 'utf-8') as file:
        json.dump({}, file, indent= 4, ensure_ascii= False)

class DataBaseWorker:
    # работа с пользователями
    @staticmethod
    def add_user(user_id: int):
        with open('data/users.json', 'r', encoding= 'utf-8') as file:
            users = json.load(file)
        
        user_id = str(user_id)
        users[user_id] = users.get(user_id, 0) + 1

        with open('data/users.json', 'w', encoding= 'utf-8') as file:
            json.dump(users, file, indent= 4, ensure_ascii= False)

    @staticmethod
    def del_user(user_id: int):
        with open('data/users.json', 'r', encoding= 'utf-8') as file:
            users = json.load(file)
        
        user_id = str(user_id)
        if users.get(user_id):
            del users[user_id]

        with open('data/users.json', 'w', encoding= 'utf-8') as file:
            json.dump(users, file, indent= 4, ensure_ascii= False)
    
    @staticmethod
    def get_users():
        with open('data/users.json','r',encoding= 'utf-8') as file:
            users = json.load(file)

        return users

    
    # работа с базой ВУЗов
    @staticmethod
    def add_vuz(name: str, urls: dict):
        with open('data/data.json', 'r', encoding= 'utf-8') as file:
            vuzes = json.load(file)
        
        vuzes[name] = urls

        with open('data/data.json', 'w', encoding= 'utf-8') as file:
            json.dump(vuzes, file, indent= 4, ensure_ascii= False)

    @staticmethod
    def get_vuzes():
        with open('data/data.json','r',encoding= 'utf-8') as file:
            vuzes = json.load(file)

        return vuzes
