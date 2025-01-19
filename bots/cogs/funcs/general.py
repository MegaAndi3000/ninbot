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
    """Generates a directory, which maps id to nick (or id to name, if nick doesn't exist).

    Args:
        bot (bot): a discord.py bot client

    Returns:
        dict: directory, which maps id (str) to nick (str)
    """

    id_to_nick = {}

    for guild in bot.guilds:
        async for member in guild.fetch_members():
            if member.nick:
                id_to_nick[str(member.id)] = member.nick
            else:
                id_to_nick[str(member.id)] = member.name

    return id_to_nick

async def get_nick_to_id(bot):
    """Generates a directory, which maps nick to id (or name to id, if nick doesn't exist).

    Args:
        bot (bot): a discord.py bot client

    Returns:
        dict: directory, which maps nick (str) to id (str)
    """
    
    nick_to_id = {}
    
    for guild in bot.guilds:
        async for member in guild.fetch_members():
            if member.nick:
                nick_to_id[member.nick] = str(member.id)
            else:
                nick_to_id[member.name] = str(member.id)
                
    return nick_to_id

def set_string_length(string:str, length:int):
    """Extends or shortens a given string to a given length.

    Args:
        string (str): string, which is to be edited
        length (int): the resulting length

    Returns:
        str: edited string with given length
    """
    
    if len(string) > length:
        new_string = string[:length]
    else:
        new_string = string + " " * (length - len(string))    
    
    return new_string

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

def sort_dic_value(dictionary:dict, sort_value:str):
    """Sorts a dictionary, which contains dictionaries by values of the latter.

    Args:
        dictionary (dict): dictionary, which is to be sorted
        sort_value (str): name of the value, by which to sort

    Returns:
        dict: sorted dictionary
    """
    
    new_dic = {}
    
    dictionaries = list(dictionary.values())
    values = []
    
    for dic in dictionaries:
        values.append(dic[sort_value])
    
    values.sort(reverse=True)
    
    for value in values:
        for key, dic in dictionary.items():
            if dic[sort_value] == value:
                if key not in new_dic:
                    new_dic[key] = dic
                    
    return new_dic
    