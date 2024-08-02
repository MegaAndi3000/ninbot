import os
import discord
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv('POLLBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

channel_list = [808968021841281074, 1105874358905356288, 805748081928306729, 836144979097157683, 1088021634125926450]

emoji = {
    'smile' : '\U0001F601',
    'like' : '\U0001F44D',
    'dislike' : '\U0001F44E',
    'laugh' : '\U0001F602',
    'red_heart' : '\U00002764',
    'green_heart' : '\U0001F49A',
    'poop' : '\U0001F4A9',
    'a' : '\U0001F1E6',
    'b' : '\U0001F1E7',
    'c' : '\U0001F1E8',
    'f' : '\U0001F1EB',
    'k' : '\U0001F1F0',
    'p' : '\U0001F1F5',
    's' : '\U0001F1F8'
    }

reactions = []
query = ''

@client.event
async def on_ready():

    print('Ready')

@client.event
async def on_message(message):

    global reactions
    global query

    if message.channel.id in channel_list:

        await message.add_reaction(emoji['like'])
        await message.add_reaction(emoji['dislike'])
        
    elif message.channel.id == 1182071341587906700:
        
        await message.add_reaction(emoji['s'])
        await message.add_reaction(emoji['p'])

    elif message.channel.id == 805757738067689502:
        
        if message.author != client.user:
            
            split = ctx.message.content
            reactions = [split[0], split[1], split[2]]
            query = split[3:]
            
            await message.delete()
            await message.send(f'<@!{str(message.author.id)}>: {query}')
            
        else:
            
            for reaction in reactions:
                
                if reaction != 'none':

                    await message.add_reaction(emoji[reaction])

client.run(TOKEN)