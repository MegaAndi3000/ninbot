import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
from random import randint
from datetime import date
from modules import sort_dic

load_dotenv()
TOKEN = os.getenv('NINBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

daily_min = 15
daily_max = 25

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
                            
                            file.write(f'{member.id}@0@1970-01-01\n')

    file_load()

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
        
        shit_coin_list[int(user)] = int(amount)
        
    file_update()

@bot.command(name='bal')
async def balance(ctx):
    
    await ctx.send(f'Du hast {shit_coin_list[ctx.author.id]} SC.')

@bot.command(name='cf')
async def coinflip(ctx, amount):
             
    if ctx.channel.id != 818574446910636072:
        
        pass
    
    else:
        
        user = ctx.author.id
        balance = shit_coin_list[user]
        
        if amount == 'all':
            
            amount = balance
            
        else:
            
            amount = int(amount)
            
        if amount > balance:
            
            response = 'Du hast nicht genügend SC.'
            
        elif amount <= 0:
            
            response = 'Du kleiner Halunke. So nicht!'
            
        else:
            
            cf = random.random()
            
            if cf >= 0.5:
                
                response = f'Glückwunsch! Du hast {str(amount)} SC gewonnen.'
                balance += amount
                
            else:
                
                response = f'Schade! Du hast {str(amount)} SC verloren. Das nächste Mal läuft es bestimmt besser!'
                balance -= amount
                
            shit_coin_list[user] = balance
            file_update()

        await ctx.send(response)
        
    file_update()

@bot.command(name='daily')
async def daily(ctx):
        
    if ctx.channel.id != 818574446910636072:
        
        pass
    
    else:
     
        user = ctx.author.id
        last_check = daily_check_list[user]
        
        today = date.today()
        
        if today == last_check:
            
            response = 'Du hast schon deine heutige Belohnung eingesammelt.'
            
        else:
            
            amount = randint(daily_min, daily_max)
            shit_coin_list[user] += amount
            daily_check_list[user] = today
            response = f'Du hast {str(amount)} SC verdient.'
            
        await ctx.send(response)
        
    file_update()
    
@bot.command(name='top')
async def top(ctx):
           
    global shit_coin_list
           
    if ctx.channel.id != 818574446910636072:
        
        pass
    
    else:

        id_to_nick = {}

        for guild in bot.guilds:
            
            if guild.name == 'Großfamilie':
                
                async for member in guild.fetch_members():
                
                    if member.bot == False:
                        
                      id_to_nick[member.id] = member.nick  

        shit_coin_list = sort_dic(shit_coin_list)
        response = ''
        
        i = 1
        
        for user in shit_coin_list:
            
            response += f'{str(i)}. {id_to_nick[user]} mit {str(shit_coin_list[user])} SC\n'
            i += 1
     
        await ctx.send(response)
     
bot.run(TOKEN)