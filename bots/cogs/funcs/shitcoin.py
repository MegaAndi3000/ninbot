import json
from dotenv import load_dotenv

def file_update(data):
                        
    with open("Data/shitcoin.json", "w") as file:
        json.dump(data, file)
    
def file_load():
    
    load_dotenv(override=True)
    
    with open("Data/shitcoin.json", "r") as file:
        data = json.load(file)
        
    return data