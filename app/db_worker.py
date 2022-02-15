import json
import os 

if not(os.path.exists('data')):
    os.mkdir('data')

if not(os.path.exists('data/data.json')):
    with open('data/data.json','w',encoding='utf-8') as file:
        json.dump({}, file, indent= 4, ensure_ascii= False)

def get_vuz(name):
    with open('data/data.json','r',encoding='utf-8') as file:
        data = json.load(file)
    
    vuz = data.get(name,0)

    return vuz

def get_data():
    with open('data/data.json','r',encoding='utf-8') as file:
        data = json.load(file)
    
    return data

def download_new_vuz(vuz:list):
    with open('data/data.json','r',encoding='utf-8') as file:
        data = json.load(file)
    
    data[vuz[0]] = vuz[1:]

    with open('data/data.json','w',encoding='utf-8') as file:
        json.dump(data, file, indent= 4, ensure_ascii= False)