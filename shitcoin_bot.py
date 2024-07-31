import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('NINBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

def file_update():
    
    with open('Data/shitcoin.txt', 'w') as file:
        
        for user in shit_coin_list:
            
            file.write(f'{user}@{str(shit_coin_list[user])}@{str(daily_check_list[user])}\n')

def file_load():
    
    global shit_coin_list
    global daily_check_list
    
    shit_coin_list = {}
    daily_check_list = {}
    
    with open('Data/shitcoin.txt') as file:
        
        lines = file.readlines()
        
        for account in lines:
            
            word_list = account.split('@')
            shit_coin_list[word_list[0]] = int(word_list[1])
            daily_check_list[word_list[0]] = int(word_list[2])

@bot.event
async def on_ready():
    
    file_load()
    print('Ready')
    
@bot.command(name='data_reset')
async def data_reset(ctx):
    
    if ctx.channel.id != 818574446910636072:
        
        pass
    
    elif ctx.author.id != 477835895702028298:
        
        await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
        
    else:
        
        with open('Data/shitcoin.txt', 'w') as file:
        
            for guild in bot.guilds:
                
                if guild.name == 'Großfamilie':
                    
                    async for member in guild.fetch_members():
                    
                        if member.bot == False:
                            
                            file.write(f'{member.id}@0@0\n')

    file_update()

@bot.command(name='show_data')
async def show_data(ctx):
            
    if ctx.channel.id != 818574446910636072:
        
        pass
    
    elif ctx.author.id != 477835895702028298:
        
        await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
    
    else:
        
        global shit_coin_list
        global daily_check_list
        
        response = ''
        
        for user in shit_coin_list:
            
            response += f'{str(user)}: {str(shit_coin_list[user])} SC, DC {str(daily_check_list[user])}\n'

    await ctx.channel.send(response)

@bot.command(name='set')
async def coin_set(ctx, user, amount):
            
    if ctx.channel.id != 818574446910636072:
        
        pass
    
    elif ctx.author.id != 477835895702028298:
        
        await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
    
    else:
        
        shit_coin_list[user] = int(amount)
        
    file_update()

bot.run(TOKEN)