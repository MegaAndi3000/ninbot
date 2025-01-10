import os
import discord
from dotenv import load_dotenv
from funcs import get_ids, get_id_to_nick

load_dotenv()
TOKEN = os.getenv('NINBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():

    print('Ready: counter')

    global current_counter
    global last_author
    global highscore
    
    with open('Data/counter.txt', 'r') as file:
        
        lines = file.readlines()
        current_counter = int(lines[0])
        last_author = int(lines[1])
        highscore = int(lines[2])
        
@client.event
async def on_message(message):

    global last_author
    global current_counter
    global highscore

    id_list = get_ids()
    
    if message.channel.id != id_list['counter'] or message.author.id == id_list['NinBot']:
        
        pass
    
    else:
        
        try:
            
            number = int(message.content)
            
            if message.author.id == last_author:
                
                await message.delete()
                
            elif number != current_counter + 1:
                
                await message.delete()
                id_to_nick = await get_id_to_nick(client)
                await message.channel.send(f"{id_to_nick[message.author.id]} hat die Streak gebrochen.")
                
                current_counter = 0
                last_author = 0
                
            else:
                
                current_counter = number
                last_author = message.author.id
                highscore = current_counter
                
            with open('Data/counter.txt', 'w') as file:
                
                file.write(f'{current_counter}\n{last_author}\n{highscore}')
            
        except ValueError:
            
            await message.delete()

client.run(TOKEN)