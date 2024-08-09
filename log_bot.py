import os
import discord
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv('NINBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():

    print('Ready')

@client.event
async def on_message(message):

    with open(f'Logs/{message.channel.id}.txt', 'a') as file:

        file.write(f'\n~ {int(time.mktime(message.created_at.timetuple()))} ~ {message.id} ~ {message.author.id} ~ {message.content}')

client.run(TOKEN)