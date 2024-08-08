import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
from random import randint
from datetime import date
from funcs import *

load_dotenv()
TOKEN = os.getenv('NINBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

def file_update():
    
    with open('Data/shitcoin.txt', 'w') as file:
        
        for user in shit_coin_list:
            
            file.write(f'{user}@{str(shit_coin_list[user])}@{daily_check_list[user]}\n')

def file_load():
    
    global shit_coin_list
    global daily_check_list
    
    shit_coin_list = {}
    daily_check_list = {}
    
    with open('Data/shitcoin.txt') as file:
        
        lines = file.readlines()

        for account in lines:
            
            word_list = account.split('@')
            shit_coin_list[int(word_list[0])] = int(word_list[1])
            daily_check_list[int(word_list[0])] = word_list[2].split('\n')[0]

@bot.event
async def on_ready():
    
    file_load()
    print('Ready')
    
@bot.command(name='data_reset')
async def data_reset(ctx):
    
    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    elif ctx.author.id != id_list['MegaAndi3000']:
        
        await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
        
    else:
        
        with open('Data/shitcoin.txt', 'w') as file:
        
            for guild in bot.guilds:
                
                if guild.name == 'Großfamilie':
                    
                    async for member in guild.fetch_members():
                    
                        if member.bot == False:
                            
                            file.write(f'{member.id}@0@1970-01-01\n')

    file_load()

@bot.command(name='show_data')
async def show_data(ctx):
            
    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    elif ctx.author.id != id_list['MegaAndi3000']:
        
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
            
    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    elif ctx.author.id != id_list['MegaAndi3000']:
        
        await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
    
    else:
        
        shit_coin_list[int(user)] = int(amount)
        
    file_update()

@bot.command(name='bal')
async def balance(ctx):
    
    await ctx.send(f'Du hast {shit_coin_list[ctx.author.id]} SC.')

@bot.command(name='daily')
async def daily(ctx):
        
    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    else:
     
        user = ctx.author.id
        last_check = daily_check_list[user]
        
        today = str(date.today())
        
        if today == last_check:
            
            response = 'Du hast schon deine heutige Belohnung eingesammelt.'
            
        else:
            
            amount = randint(int(os.getenv('DAILY_MIN')), int(os.getenv('DAILY_MAX')))
            shit_coin_list[user] += amount
            daily_check_list[user] = today
            response = f'Du hast {str(amount)} SC verdient.'
            
        await ctx.send(response)
        
    file_update()
    
@bot.command(name='top')
async def top(ctx):
        
    global shit_coin_list
    id_list = get_ids()
           
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    else:

        id_to_nick = await get_id_to_nick(bot)

        shit_coin_list = sort_dic(shit_coin_list)
        response = ''
        
        i = 1
        
        for user in shit_coin_list:
            
            if shit_coin_list[user] > 0:
                
                response += f'{str(i)}. {id_to_nick[user]} mit {str(shit_coin_list[user])} SC\n'
                i += 1
     
        await ctx.send(response)

@bot.command(name='gift')
async def gift(ctx, target, amount):
    
    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass

    else:
        
        nick_to_id = await get_nick_to_id(bot)
        user = ctx.author.id
        amount = int(amount)
        
        if amount > shit_coin_list[user]:
            
            response = 'Du hast nicht genügend SC dafür.'
            
        elif amount <= 0:
            
            response = 'Du kleiner Halunke. So nicht!'
            
        else:
            
            target_id = nick_to_id[target]
            shit_coin_list[user] -= amount
            shit_coin_list[target_id] += amount
            
            response = f'Du hast {target} {amount} SC geschenkt.'

        file_update()
        await ctx.send(response)            
        
@bot.command(name='add_user')
async def add_user(ctx, target):

    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    elif ctx.author.id != id_list['MegaAndi3000']:
            
        await ctx.send('Du bist dazu nicht berechtigt. Sorry!')
        
    else:
        
        shit_coin_list[int(target)] = 0
        file_update()
        await ctx.send(f'User {int(target)} wurde hinzugefügt.')
        
bot.run(TOKEN)