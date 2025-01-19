import os
from discord.ext import commands
from cogs.funcs.general import get_ids, get_id_to_nick, get_nick_to_id, sort_dic
from cogs.funcs.shitcoin import file_load, update
from random import choice, random, randint
from datetime import date
import time

class Shitcoin_Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bal', help='Zeigt deinen aktuellen SC-Stand an.')
    async def balance(self, ctx):
        
        shit_coin_list = file_load()[0]
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return

        if shit_coin_list[ctx.author.id] == 0:        
            await ctx.send('Du bist leider broke. Schade Marmelade!')
        else:
            await ctx.send(f'Du hast {shit_coin_list[ctx.author.id]} SC.')

    @commands.command(name='bet', help='Setze deine SC in einer Art Lotterie aufs Spiel.')
    async def bet(self, ctx, amount):
        
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        user = ctx.author.id
        
        if ctx.channel.id != id_list['shitcoin']:
            return
        
        if amount == 'all':
            amount = shit_coin_list[user]
        else:
            amount = int(amount)   
        
        if amount > shit_coin_list[user]:
            await ctx.send('Du hast nicht genügend SC dafür.')
            return
        elif amount < 10:
            await ctx.send('Du musst mindestens 10 SC einsetzen.')
            return

        prize_list = [5] * 1 + [2] * 24 + [1] * 20 + [0.5] * 34 + [0] * 21
        answer_list = {5: 'Jackpot! Du hast [amount] SC gewonnen!',
                    2: 'Du hast Glück! Du hast [amount] SC gewonnen!',
                    1: 'Du hast nichts gewonnen, aber auch nichts verloren.',
                    0.5: 'Na immerhin...du hast nur [amount] SC verloren.',
                    0: 'Niete! Du hast leider [amount] SC verloren.'}
        
        shit_coin_list[user] -= amount
        prize = choice(prize_list)
        reward = int(amount * prize)
        shit_coin_list[user] = int(shit_coin_list[user] + reward)
        
        update(shit_coin_list, daily_check_list, steal_check_list, all_time_top_list)
        
        response = answer_list[prize].replace('[amount]', f'{abs(amount - reward)}')
        await ctx.send(response)

    @commands.command(name='cf', help='Setze deine SC beim Münzwurf aufs Spiel.')
    async def coinflip(self, ctx, amount):
                
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return
    
        user = ctx.author.id
        balance = shit_coin_list[user]
        
        if amount == 'all':            
            amount = balance
        else:
            amount = int(amount)
            
        if amount > balance:
            await ctx.send('Du hast nicht genügend SC.')
            return
        elif amount <= 0:
            await ctx.send('Du kleiner Halunke. So nicht!')
            return

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
        update(shit_coin_list, daily_check_list, steal_check_list, all_time_top_list)
        await ctx.send(response)

    @commands.command(name='cf_history', help='Zeigt die Gesamtbilanz der Münzwürfe.')
    async def coinflip_history(self, ctx):
        
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return

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

        await ctx.send(f'cf-Durchschnitt: {sum/count_total:.5f}\nQuote: {count}/{count_total} = {count/count_total:.5f}')

    @commands.command(name='daily', help='Gibt dir eine zufällige tägliche Belohnung.')
    async def daily(self, ctx):
        
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return
        
        user = ctx.author.id
        last_check = daily_check_list[user]
        today = str(date.today())
        
        if today == last_check:
            await ctx.send('Du hast schon deine heutige Belohnung eingesammelt.')
            return
        elif user == id_list['Tobi2']:
            await ctx.send('Du kleiner Racker!')
            return
            
        amount = randint(int(os.getenv('DAILY_MIN')), int(os.getenv('DAILY_MAX')))
        shit_coin_list[user] += amount
        daily_check_list[user] = today
        response = f'Du hast {amount} SC verdient.'
        await ctx.send(response)
        
        update(shit_coin_list, daily_check_list, steal_check_list, all_time_top_list)

    @commands.command(name='gift', help='Schenke einem anderen User SC.')
    async def gift(self, ctx, *args):
        
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        
        args = list(args)
        amount = args[-1]
        args.pop(-1)
        target = ' '.join(args)
        
        if ctx.channel.id != id_list['shitcoin']:
            return

        nick_to_id = await get_nick_to_id(self.bot)
        user = ctx.author.id
        
        if amount == 'all':
            amount = shit_coin_list[user]
        else:
            amount = int(amount)

        if amount > shit_coin_list[user]:
            await ctx.send('Du hast nicht genügend SC dafür.')
            return
        elif amount <= 0:
            await ctx.send('Du kleiner Halunke. So nicht!')
            return
    
        target_id = nick_to_id[target]
        shit_coin_list[user] -= amount
        shit_coin_list[target_id] += amount
        
        response = f'Du hast {target} {amount} SC geschenkt.'

        update(shit_coin_list, daily_check_list, steal_check_list, all_time_top_list)
        await ctx.send(response)            

    @commands.command(name='steal', help='Stiehl einer anderen Person ihre hart erarbeiteten SC.')
    async def steal(self, ctx, target):

        if ctx.channel.id != id_list['shitcoin']:
            return
        
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        id_to_nick = await get_id_to_nick(self.bot)
        nick_to_id = await get_nick_to_id(self.bot)
        user = ctx.author.id
        target = nick_to_id[target]
                
        if user == id_list['Tobi2']:
            await ctx.send('Zeitlimits sind nicht dafür da, umgangen zu werden!')
            return
    
        current_time = time.time()
        
        if current_time < steal_check_list[user] + int(os.getenv('STEAL_COOLDOWN')):
            time_difference = int(os.getenv('STEAL_COOLDOWN')) - (current_time - steal_check_list[user])
            await ctx.send(f'Du kannst nur einmal pro Stunde ein solches Unterfangen starten. Probiere es in {int(time_difference // 60)} min {int(time_difference % 60)} s erneut.')
            return
        elif shit_coin_list[target] < 100 or shit_coin_list[target] < 0.5 * shit_coin_list[user]:    
            # Robin Hood clause
            await ctx.send('Robin Hood stiehlt nicht von den Armen und du sollst das auch nicht tun.')
            return
        elif shit_coin_list[user] < int(float(os.getenv('STEAL_COST_FACTOR')) * shit_coin_list[target]):
            await ctx.send(f'Du brauchst {int(float(os.getenv('STEAL_COST_FACTOR')) * shit_coin_list[target])} SC dafür. Fluchtwagen bezahlen sich nicht von alleine!')
            return
        
        cost = int(float(os.getenv('STEAL_COST_FACTOR')) * shit_coin_list[target])
        shit_coin_list[user] -= cost
        steal_check_list[user] = current_time
        steal_value = random()
        
        with open('Logs/steal.txt','a') as file:
            file.write(f'{steal_value}\n')
        
        if steal_value <= float(os.getenv('STEAL_PIVOT')):
            loot = int(float(os.getenv('STEAL_AMOUNT')) * shit_coin_list[target])
            shit_coin_list[target] -= loot
            shit_coin_list[user] += loot
            response = f'Du hast {loot} SC von {id_to_nick[target]} gestohlen. Abzüglich der Fluchtwagenkosten beläuft sich dein Gewinn auf {int(loot - cost)} SC.'
        else:
            response = f'Du warst leider nicht erfolgreich. Die {cost} SC für die Fluchtwagen musst du trotzdem zahlen. Aber immerhin gibt es hier kein Justizsystem.'
            
        update(shit_coin_list, daily_check_list, steal_check_list, all_time_top_list)
        await ctx.send(response)

    @commands.command(name='top', help='Zeigt die aktuelle und all time Rangliste an.')
    async def top(self, ctx):
            
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
            
        if ctx.channel.id != id_list['shitcoin']:
            return
        
        id_to_nick = await get_id_to_nick(self.bot)

        shit_coin_list = sort_dic(shit_coin_list)
        all_time_top_list = sort_dic(all_time_top_list)

        response = '=== AKTUELL ===\n\n'
        i = 1
        for user in shit_coin_list:
            if user not in id_to_nick:
                id_to_nick[user] = (await self.bot.fetch_user(user)).name
            if shit_coin_list[user] > 0:
                response += f'{i}. {id_to_nick[user]} mit {shit_coin_list[user]} SC\n'
                i += 1
                
        response += '\n=== ALL-TIME ===\n\n'
        i = 1
        for user in all_time_top_list:
            if i <= 5:
                response += f'{i}. {id_to_nick[user]} mit {all_time_top_list[user]} SC\n'
            i += 1
    
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Shitcoin_Users(bot))