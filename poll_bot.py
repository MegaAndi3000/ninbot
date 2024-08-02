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
    'smile': '\U0001F601',
    'like': '\U0001F44D',
    'dislike': '\U0001F44E'}

@client.event
async def on_ready():

    print('Ready')

@client.event
async def on_message(message):

    if message.channel.id in channel_list:

        await message.add_reaction(emoji['like'])
        await message.add_reaction(emoji['dislike'])

client.run(TOKEN)