from dotenv import load_dotenv

def update(shit_coin_list, daily_check_list, steal_check_list, all_time_top_list):
                        
    for user in shit_coin_list:
        
        if shit_coin_list[user] > all_time_top_list[user]:
            
            all_time_top_list[user] = shit_coin_list[user]
    
    with open('Data/shitcoin.txt', 'w') as file:
        
        for user in shit_coin_list:
            
            file.write(f'{user}@{int(shit_coin_list[user])}@{daily_check_list[user]}@{int(steal_check_list[user])}@{int(all_time_top_list[user])}\n')

def file_load():
    
    load_dotenv(override=True)
    
    shit_coin_list = {}
    daily_check_list = {}
    steal_check_list = {}
    all_time_top_list = {}
    
    with open('Data/shitcoin.txt') as file:
        
        lines = file.readlines()

        for account in lines:
            
            word_list = account.split('@')
            shit_coin_list[int(word_list[0])] = int(word_list[1])
            daily_check_list[int(word_list[0])] = word_list[2]
            steal_check_list[int(word_list[0])] = int(word_list[3])
            all_time_top_list[int(word_list[0])] = int(word_list[4])

    return shit_coin_list, daily_check_list, steal_check_list, all_time_top_list