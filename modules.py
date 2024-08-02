def sort_dic(dictionary):
    
    new_dic = {}
    
    values = list(dictionary.values())
    values.sort(reverse=True)
    
    for value in values:
        
        for key in dictionary:
            
            if dictionary[key] == value:
                
                if key not in new_dic:
                    
                    new_dic[key] = value
                    
    return new_dic

def get_params():
    
    params = {}
    
    with open('.params.txt', 'r') as file:
        
        lines = file.readlines()

        for line in lines:
            
            split = line.split('=')
            params[split[0]] = float(split[1])
            
    return params

async def get_id_to_nick(bot):

    id_to_nick = {}

    for guild in bot.guilds:
        
        if guild.id == 805743762885443594:
            
            async for member in guild.fetch_members():
            
                if member.bot == False:
                    
                    id_to_nick[member.id] = member.nick  

    return id_to_nick

async def get_nick_to_id(bot):
    
    nick_to_id = {}
    
    for guild in bot.guilds:
        
        if guild.id == 805743762885443594:
            
            async for member in guild.fetch_members():
                
                if member.bot == False:
                    
                    nick_to_id[member.nick] = member.id
                    
    return nick_to_id