import os
import discord
from dotenv import load_dotenv
from funcs import get_ids

load_dotenv()
TOKEN = os.getenv('NINBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():

    print('Ready: basic_counter')

    global current_counter
    global last_author
    
    with open('Data/basic_counter.txt', 'r') as file:
        
        lines = file.readlines()
        current_counter = int(lines[0])
        last_author = int(lines[1])
        
@client.event
async def on_message(message):

    global last_author
    global current_counter

    id_list = get_ids()
    
    if message.channel.id != id_list['basic-counter']:
        
        pass
    
    else:
        
        try:
            
            number = int(message.content)
            
            if message.author.id == last_author:
                
                await message.delete()
                
            elif number != current_counter + 1:
                
                await message.delete()
                
            else:
                
                current_counter = number
                last_author = message.author.id
                
                with open('Data/basic_counter.txt', 'w') as file:
                
                    file.write(f'{current_counter}\n{last_author}')
            
        except ValueError:
            
            await message.delete()

client.run(TOKEN)