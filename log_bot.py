import os
import discord
from dotenv import load_dotenv
import time
from datetime import datetime

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

@client.event
async def on_raw_message_edit(event):

    with open('Logs/edits.txt', 'a') as file:
        
        file.write(f'\n~ {int(time.mktime(time.strptime(event.data['edited_timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')))} ~ {event.channel_id} ~ {event.message_id} ~ {event.data['author']['id']} ~ {event.data['content']}')

client.run(TOKEN)