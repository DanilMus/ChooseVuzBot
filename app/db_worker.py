import json
import os 

if not(os.path.exists('data/data.json')):
    with open('data/data.json','w',encoding='utf-8') as file:
        json.dump({}, file, indent= 4, ensure_ascii= False)

def get_data():
    with open('data/data.json','r',encoding='utf-8') as file:
        data = json.load(file)
    
    return data

def rewrite_data(data):
    with open('data/data.json','w',encoding='utf-8') as file:
        json.dump(data, file, indent= 4, ensure_ascii= False)

def push_data(data):
    with open('data/data.json','a',encoding='utf-8') as file:
        json.dump(data, file, indent= 4, ensure_ascii= False)