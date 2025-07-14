import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.funcs.general import get_ids

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('POLLBOT_TOKEN')

bot = commands.Bot(command_prefix='?', intents=intents)

reactions = []
query = ''
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

class Pollbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def react(self, message):

        global reactions
        global query
        id_list = get_ids()

        channel_list = [id_list['zitate'],
                        id_list['memes-und-witze'],
                        id_list['suesse-tiere'],
                        id_list['katzenbilder'],
                        id_list['atelier']]

        if message.channel.id in channel_list:
            await message.add_reaction(emoji['like'])
            await message.add_reaction(emoji['dislike'])
            
        elif message.channel.id == id_list['smash-or-pass']:
            await message.add_reaction(emoji['s'])
            await message.add_reaction(emoji['p'])

        elif message.channel.id == id_list['umfragen']:
            if message.author != self.bot.user:
                
                split = message.content.split()
                reactions = [split[0], split[1], split[2]]
                query = ' '.join(split[3:])
                
                await message.delete()
                await message.channel.send(f'<@!{message.author.id}>: {query}')
                
            else:
                for reaction in reactions:
                    if reaction != 'none':
                        await message.add_reaction(emoji[reaction])

@bot.event
async def on_ready():
    
    await bot.add_cog(Pollbot(bot))
    
bot.run(TOKEN)