def sort_dic(dictionary:dict):
    """Sorts a directory by its values

    Args:
        dictionary (dict): directory, which is to be sorted

    Returns:
        dict: sorted dictory
    """
    
    new_dic = {}
    
    values = list(dictionary.values())
    values.sort(reverse=True)
    
    for value in values:
        
        for key in dictionary:
            
            if dictionary[key] == value:
                
                if key not in new_dic:
                    
                    new_dic[key] = value
                    
    return new_dic

def get_ids():
    """Reads the ids of channels und users from '.ids'.

    Returns:
        dict: directory, which maps name (str) to id (int)
    """
    
    id_dict = {}
    
    with open('.ids', 'r') as file:
        
        lines = file.readlines()
        
        for line in lines:
        
            if len(line) > 2:
            
                split = line.split(' = ')    
                id_dict[split[0]] = int(split[1])
                
    return id_dict

async def get_id_to_nick(bot):
    """Generates a directory, which maps id to nick.

    Args:
        bot (bot): a discord.py bot client

    Returns:
        dict: directory, which maps id (int) to nick (str)
    """

    id_to_nick = {}

    for guild in bot.guilds:
        
        if guild.id == 805743762885443594:
            
            async for member in guild.fetch_members():
            
                if member.bot == False:
                    
                    id_to_nick[member.id] = member.nick  

    return id_to_nick

async def get_nick_to_id(bot):
    """Generates a directory, which maps nick to id.

    Args:
        bot (bot): a discord.py bot client

    Returns:
        dict: directory, which maps nick (str) to id (int)
    """
    
    nick_to_id = {}
    
    for guild in bot.guilds:
        
        if guild.id == 805743762885443594:
            
            async for member in guild.fetch_members():
                
                if member.bot == False:
                    
                    nick_to_id[member.nick] = member.id
                    
    return nick_to_id