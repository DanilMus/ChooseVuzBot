import json
import os 

if not(os.path.exists('data')):
    os.mkdir('data')

if not(os.path.exists('data/data.json')):
    with open('data/data.json','w',encoding='utf-8') as file:
        json.dump({}, file, indent= 4, ensure_ascii= False)

def get_vuz(name):
    with open('tests/a.json','r',encoding='utf-8') as file:
        data = json.load(file)
    
    vuz = data.get(name,0)

    return vuz

def download_vuzes(vuzes:dict):
    with open('tests/a.json','r',encoding='utf-8') as file:
        data = json.load(file)
    
    for key, val in vuzes.items():
        data[key] = val

    with open('tests/a.json','w',encoding='utf-8') as file:
        json.dump(data, file, indent= 4, ensure_ascii= False)