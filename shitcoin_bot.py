import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from random import random, randint, choice
from datetime import date
import time
from funcs import *

load_dotenv()
TOKEN = os.getenv('NINBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

def update():
    
    for user in shit_coin_list:
        
        if shit_coin_list[user] > all_time_top_list[user]:
            
            all_time_top_list[user] = shit_coin_list[user]
    
    with open('Data/shitcoin.txt', 'w') as file:
        
        for user in shit_coin_list:
            
            file.write(f'{user}@{int(shit_coin_list[user])}@{daily_check_list[user]}@{int(steal_check_list[user])}@{int(all_time_top_list[user])}\n')

def file_load():
    
    global shit_coin_list
    global daily_check_list
    global steal_check_list
    global all_time_top_list
    
    shit_coin_list = {}
    daily_check_list = {}
    steal_check_list = {}
    all_time_top_list = {}
    
    with open('Data/shitcoin.txt') as file:
        
        lines = file.readlines()

        for account in lines:
            
            word_list = account.split('@')
            shit_coin_list[int(word_list[0])] = int(word_list[1])
            daily_check_list[int(word_list[0])] = word_list[2]
            steal_check_list[int(word_list[0])] = int(word_list[3])
            all_time_top_list[int(word_list[0])] = int(word_list[4])

@bot.event
async def on_ready():
    
    file_load()
    print('Ready')
    
@bot.command(name='data_reset', help='DEBUG: Setzt alle Daten zurück.')
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
                            
                            file.write(f'{member.id}@0@1970-01-01@0@0\n')

    file_load()

@bot.command(name='show_data', help='DEBUG: Zeigt alle Daten an.')
async def show_data(ctx):
            
    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    elif ctx.author.id != id_list['MegaAndi3000']:
        
        await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
    
    else:
        
        response = ''
        
        for user in shit_coin_list:
            
            response += f'{user}: {shit_coin_list[user]} SC, DC {daily_check_list[user]}, SC {steal_check_list[user]}, T {all_time_top_list[user]}\n'

    await ctx.channel.send(response)

@bot.command(name='set', help='DEBUG: Setzt die SC eines Users auf einen bestimmten Wert.')
async def coin_set(ctx, user, amount):
            
    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    elif ctx.author.id != id_list['MegaAndi3000']:
        
        await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
    
    else:
        
        shit_coin_list[int(user)] = int(amount)
        
    update()

@bot.command(name='bal', help='Zeigt deinen aktuellen SC-Stand an.')
async def balance(ctx):
    
    await ctx.send(f'Du hast {shit_coin_list[ctx.author.id]} SC.')

@bot.command(name='daily', help='Gibt dir eine zufällige tägliche Belohnung.')
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
            response = f'Du hast {amount} SC verdient.'
            
        await ctx.send(response)
        
    update()
    
@bot.command(name='top', help='Zeigt die aktuelle und all time Rangliste an.')
async def top(ctx):
        
    global shit_coin_list
    global all_time_top_list
    
    id_list = get_ids()
           
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    else:

        id_to_nick = await get_id_to_nick(bot)

        shit_coin_list = sort_dic(shit_coin_list)
        all_time_top_list = sort_dic(all_time_top_list)
        response = '=== AKTUELL ===\n\n'
        
        i = 1
        
        for user in shit_coin_list:
            
            if shit_coin_list[user] > 0:
                
                response += f'{i}. {id_to_nick[user]} mit {shit_coin_list[user]} SC\n'
                i += 1
                
        response += '\n=== ALL-TIME ===\n\n'
        
        i = 1
        
        for user in all_time_top_list:
            
            if i <= 5:
                
                response += f'{i}. {id_to_nick[user]} mit {shit_coin_list[user]} SC\n'
                
            i += 1
     
        await ctx.send(response)

@bot.command(name='gift', help='Schenke einem anderen User SC.')
async def gift(ctx, *args):
    
    id_list = get_ids()
    
    args = list(args)
    amount = int(args[-1])
    args.pop(-1)
    target = ' '.join(args)
    
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

        update()
        await ctx.send(response)            
        
@bot.command(name='add_user', help='DEBUG: Fügt einen neuen Nutzer hinzu.')
async def add_user(ctx, target):

    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    elif ctx.author.id != id_list['MegaAndi3000']:
            
        await ctx.send('Du bist dazu nicht berechtigt. Sorry!')
        
    else:
        
        user = int(target)
        
        shit_coin_list[user] = 0
        daily_check_list[user] = '1970-01-01'
        steal_check_list[user] = 0
        all_time_top_list[user] = 0
        update()
        await ctx.send(f'User {int(target)} wurde hinzugefügt.')
        
@bot.command(name='bet', help='Setze deine SC in einer Art Lotterie aufs Spiel.')
async def bet(ctx, amount):
    
    id_list = get_ids()
    user = ctx.author.id
    
    if amount == 'all':
        
        amount = shit_coin_list[user]
        
    else:
    
        amount = int(amount)   
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    elif amount > shit_coin_list[user]:
        
        await ctx.send('Du hast nicht genügend SC dafür.')
        
    elif amount < 10:
        
        await ctx.send('Du musst mindestens 10 SC einsetzen.')
        
    else:
        
        prize_list = [5] * 1 + [2] * 24 + [1] * 20 + [0.5] * 34 + [0] * 21
        answer_list = {5: 'Jackpot! Du hast [amount] SC gewonnen!',
                       2: 'Du hast Glück! Du hast [amount] SC gewonnen!',
                       1: 'Du bekommst ein Freilos!',
                       0.5: 'Na immerhin...du hast [amount] SC gewonnen.',
                       0: 'Niete! Naja...'}
        
        shit_coin_list[user] -= amount
        prize = choice(prize_list)
        reward = int(amount * prize)
        shit_coin_list[user] = int(shit_coin_list[user] + reward)
        
        update()
        
        response = answer_list[prize].replace('[amount]', f'{reward}')
        
        await ctx.send(response)
        
@bot.command(name='cf', help='Setze deine SC beim Münzwurf aufs Spiel.')
async def coinflip(ctx, amount):
            
    id_list = get_ids()
     
    if ctx.channel.id != id_list['shitcoin']:
        
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
            
            cf_value = random()
            
            with open('Logs/coinflip.txt', 'a') as file:
                
                file.write(str(cf_value)+'\n')
                
            if cf_value >= float(os.getenv('CF_PIVOT')):
                
                response = f'Glückwunsch! Du hast {amount} SC gewonnen.'
                balance += amount
                
            else:
                
                response = f'Schade! Du hast {amount} SC verloren. Das nächste Mal läuft es bestimmt besser!'
                balance -= amount
                
            shit_coin_list[user] = balance
            update()

        await ctx.send(response)
        
    update()
    
@bot.command(name='cf_history', help='Zeigt die Gesamtbilanz der Münzwürfe.')
async def coinflip_history(ctx):
    
    id_list = get_ids()
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass

    else:
        
        count_total = 0
        count = 0
        sum = 0
        
        with open('Logs/coinflip.txt', 'r') as file:
            
            lines = file.readlines()
            count_total = len(lines)
            
            for line in lines:
                          
                sum += float(line)
                
                if float(line) >= 0.5:
                    
                    count += 1
                
        await ctx.send(f'cf-Durchschnitt: {sum/count_total}\nQuote: {count}/{count_total} = {count/count_total}')

@bot.command(name='steal', help='Stiehl einer anderen Person ihre hart erarbeiteten SC.')
@commands.cooldown(1, 300, commands.BucketType.user)
async def steal(ctx, target):
    
    id_list = get_ids()
    id_to_nick = await get_id_to_nick(bot)
    nick_to_id = await get_nick_to_id(bot)
    user = ctx.author.id
    target = nick_to_id[target]
    
    if ctx.channel.id != id_list['shitcoin']:
        
        pass
    
    else:
        
        current_time = time.time()
        
        if current_time < steal_check_list[user] + int(os.getenv('STEAL_COOLDOWN')):
        
            time_difference = current_time - steal_check_list[user] - int(os.getenv('STEAL_COOLDOWN'))
            response = f'Du kannst nur einmal pro Stunde ein solches Unterfangen starten. Probiere es in {time_difference // 60} min {time_difference % 60} s erneut.'
        
        elif shit_coin_list[target] < 100:
            
            response = 'Robin Hood stiehlt nicht von den Armen und du sollst das auch nicht tun.'
            
        elif shit_coin_list[user] < int(0.1 * shit_coin_list[target]):
            
            response = f'Du brauchst {int(0.1 * shit_coin_list[target])} SC dafür. Fluchtwagen bezahlen sich nicht von alleine!'
            
        else:
            
            cost = int(0.1 * shit_coin_list[target])
            shit_coin_list[user] -= cost
            steal_check_list[user] = current_time
            
            steal_value = random()
            
            with open('Logs/steal.txt','a') as file:
                
                file.write(f'{steal_value}\n')
            
            if steal_value <= float(os.getenv('STEAL_PIVOT')):
                
                loot = int(0.42 * shit_coin_list[target])
                shit_coin_list[target] -= loot
                shit_coin_list[user] += loot
                
                response = f'Du hast {loot} SC von {id_to_nick[target]} gestohlen. Abzgl. Kapitalerwerbssteuer beläuft sich dein Gewinn auf {int(loot - cost)} SC.'
                
            else:
                
                response = f'Du warst leider nicht erfolgreich. Die {cost} SC für die Fluchtwagen musst du trotzdem zahlen. Aber immerhin gibt es hier kein Justizsystem.'
                
        update()
        await ctx.send(response)

bot.run(TOKEN)