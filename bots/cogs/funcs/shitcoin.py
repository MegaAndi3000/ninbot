import json
import time
from dotenv import load_dotenv

def file_update(data):

    for user, balance in data["shit_coin_list"].items():
        if balance == int(balance):
            data["shit_coin_list"][user] = int(balance)
        if balance > data["all_time_top_list"][user]:
            data["all_time_top_list"][user] = balance

    with open("Data/shitcoin.json", "w") as file:
        json.dump(data, file)
    
def file_load():
    
    load_dotenv(override=True)
    
    with open("Data/shitcoin.json", "r") as file:
        data = json.load(file)
        
    return data

def log_event(event:str, data:dict):
    
    data_string = " ".join([f"{key}:{value}" for key, value in data.items()])
    
    with open("Data/shitcoin_events.txt", "a") as file:
        file.write(f"{event} ~ {int(time.time())} ~ {data_string}\n")