import os
from discord.ext import commands
from cogs.funcs.general import get_ids, get_id_to_nick, get_nick_to_id, sort_dic
from cogs.funcs.shitcoin import file_load, file_update, log_event
from random import choice, random, randint
from datetime import date
import time

def norm_float(input):
    """Cleans a str/float and returns float/int depending on value."""
    number = float(input)
    if number == int(number):
        number = int(number)
    return number

class Shitcoin_Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = file_load()
        self.nick_to_id = {}
        self.id_to_nick = {}
    
    async def cog_check(self, ctx):
        id_list = get_ids()
        user = str(ctx.author.id)
        return (ctx.channel.id == id_list['shitcoin'] and user in self.data['shit_coin_list'])
        
    async def cog_before_invoke(self, ctx):
        self.data = file_load()
        self.nick_to_id = await get_nick_to_id(self.bot)
        self.id_to_nick = await get_id_to_nick(self.bot)
        
    async def cog_after_invoke(self, ctx):
        file_update(self.data)

    @commands.command(name='bal', help='Zeigt deinen aktuellen SC-Stand an.')
    async def balance(self, ctx):

        user = str(ctx.author.id)
        amount = norm_float(self.data['shit_coin_list'][user])

        if amount == 0:        
            await ctx.send('Du bist leider broke. Schade Marmelade!')
        else:
            await ctx.send(f"Du hast {amount} SC.")

    @commands.command(name='bet', help='Setze deine SC in einer Art Lotterie aufs Spiel.')
    async def bet(self, ctx, amount):
        
        user = str(ctx.author.id)
        
        if amount == 'all':
            amount = self.data['shit_coin_list'][user]
        amount = norm_float(amount)
        
        if amount > self.data['shit_coin_list'][user]:
            await ctx.send('Du hast nicht genügend SC dafür.')
            return
        elif amount < 1:
            await ctx.send('Du musst mindestens 1 SC einsetzen.')
            return

        # This could be done better. Like handled externally and stuff...
        prize_list = [5] * 1 + [2] * 24 + [1] * 20 + [0.5] * 34 + [0] * 21
        answer_list = {5: 'Jackpot! Du hast [amount] SC gewonnen!',
                    2: 'Du hast Glück! Du hast [amount] SC gewonnen!',
                    1: 'Du hast nichts gewonnen, aber auch nichts verloren.',
                    0.5: 'Na immerhin...du hast nur [amount] SC verloren.',
                    0: 'Niete! Du hast leider [amount] SC verloren.'}
        
        self.data['shit_coin_list'][user] -= amount
        prize = choice(prize_list)
        reward = amount * prize
        self.data['shit_coin_list'][user] = self.data['shit_coin_list'][user] + reward

        log_event("bet", {"user": user, "amount": amount, "prize": prize})
        await ctx.send(answer_list[prize].replace('[amount]', f'{norm_float(abs(amount - reward))}'))

    @commands.command(name='cf', help='Setze deine SC beim Münzwurf aufs Spiel.')
    async def coinflip(self, ctx, amount):

        user = str(ctx.author.id)
        
        balance = self.data['shit_coin_list'][user]
        if amount == 'all':
            amount = balance
        amount = norm_float(amount)
        
        if amount > balance:
            await ctx.send('Du hast nicht genügend SC.')
            return
        elif amount <= 0:
            await ctx.send('Du kleiner Halunke. So nicht!')
            return
        elif amount < 1:
            await ctx.send('Ein Mindesteinsatz von 1 SC ist leider Vorschrift.')
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
            
        self.data['shit_coin_list'][user] = balance
        log_event("coinflip", {"user": user, "amount": amount, "cf_value": cf_value, "cf_pivot": os.getenv('CF_PIVOT')})
        await ctx.send(response)

    @commands.command(name='cf_history', help='Zeigt die Gesamtbilanz der Münzwürfe.')
    async def coinflip_history(self, ctx):

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
        
        user = str(ctx.author.id)
        last_check = self.data['daily_check_list'][user]
        today = str(date.today())
        
        if today == last_check:
            await ctx.send('Du hast schon deine heutige Belohnung eingesammelt.')
            return
            
        amount = randint(int(os.getenv('DAILY_MIN')), int(os.getenv('DAILY_MAX')))
        self.data['shit_coin_list'][user] += amount
        self.data['daily_check_list'][user] = today
        
        log_event("daily", {"user": user, "amount": amount})
        await ctx.send(f'Du hast {amount} SC verdient.')

    @commands.command(name='gift', help='Schenke einem anderen User SC.')
    async def gift(self, ctx, *args):
        
        user = str(ctx.author.id)
        
        args = list(args)
        amount = args[-1]
        args.pop(-1)
        target = ' '.join(args)
        
        if amount == 'all':
            amount = self.data['shit_coin_list'][user]
        else:
            amount = int(amount)  # No float handling to prevent leaderboard griefing

        if amount > self.data['shit_coin_list'][user]:
            await ctx.send('Du hast nicht genügend SC dafür.')
            return
        elif amount <= 0:
            await ctx.send('Du kleiner Halunke. So nicht!')
            return
    
        target_id = self.nick_to_id[target]
        
        if target_id not in self.data['shit_coin_list']:
            await ctx.send(f'Ich kenne keinen User names {target}.')
            return
        
        self.data['shit_coin_list'][user] -= amount
        self.data['shit_coin_list'][target_id] += amount
        
        response = f'Du hast {target} {amount} SC geschenkt.'

        log_event("gift", {"user": user, "target": target, "amount": amount})
        await ctx.send(response)

    @commands.command(name='round', help='Rundet dein Vermögen auf eine ganze Zahl ab.')
    async def round(self, ctx):

        user = str(ctx.author.id)
        self.data["shit_coin_list"][user] = int(self.data["shit_coin_list"][user])    
        await ctx.send("Dein Vermögen wurde erfolgreich abgerundet.")
    
    @commands.command(name='steal', help='Stiehl einer anderen Person ihre hart erarbeiteten SC.')
    async def steal(self, ctx, *args):

        user = str(ctx.author.id)
        target = ' '.join(args)
        target_id = self.nick_to_id[target]
        
        if target_id not in self.data['shit_coin_list']:
            await ctx.send(f'Ich kenne keinen User names {target}.')
            return
    
        current_time = time.time()
        cost = int(float(os.getenv('STEAL_COST_FACTOR')) * self.data['shit_coin_list'][target_id])
        
        # This looks a bit chonky. divmod or stuff might help?
        if current_time < self.data['steal_check_list'][user] + int(os.getenv('STEAL_COOLDOWN')):
            time_difference = int(os.getenv('STEAL_COOLDOWN')) - (current_time - self.data['steal_check_list'][user])
            if time_difference < 3600:
                await ctx.send(f'Der Fluchtwagen muss noch geladen werden. Probiere es in {int(time_difference // 60)} min {int(time_difference % 60)} s erneut.')
            else:
                await ctx.send(f'Das ist gerade kein guter Zeitpunkt. Probiere es in {int(time_difference // 3600)} h {int((time_difference % 3600) // 60)} min erneut.')
            return
        elif self.data['shit_coin_list'][target_id] < 100 or self.data['shit_coin_list'][target_id] < 0.5 * self.data['shit_coin_list'][user]:    
            # Robin Hood clause
            await ctx.send('Robin Hood stiehlt nicht von den Armen und du sollst das auch nicht tun.')
            return
        elif self.data['shit_coin_list'][user] < cost:
            await ctx.send(f"Du brauchst {cost} SC dafür. Fluchtwagen bezahlen sich nicht von alleine!")
            return
        
        self.data['shit_coin_list'][user] -= cost
        self.data['steal_check_list'][user] = current_time
        steal_value = random()
        
        if steal_value <= float(os.getenv('STEAL_PIVOT')):
            loot = int(float(os.getenv('STEAL_AMOUNT')) * self.data['shit_coin_list'][target_id])
            self.data['shit_coin_list'][target_id] -= loot
            self.data['shit_coin_list'][user] += loot
            response = f'Du hast {loot} SC von {target} gestohlen. Abzüglich der Fluchtwagenkosten beläuft sich dein Gewinn auf {int(loot - cost)} SC.'
        else:
            loot = 0
            response = f'Du warst leider nicht erfolgreich. Die {cost} SC für die Fluchtwagen musst du trotzdem zahlen. Aber immerhin gibt es hier kein Justizsystem.'
            
        log_event("steal", {"user": user, "target": target, "cost": cost, "loot": loot, "steal_value": steal_value, "pivot": os.getenv("STEAL_PIVOT")})
        await ctx.send(response)

    @commands.command(name='top', help='Zeigt die aktuelle und all time Rangliste an.')
    async def top(self, ctx):

        self.data['shit_coin_list'] = sort_dic(self.data['shit_coin_list'])
        self.data['all_time_top_list'] = sort_dic(self.data['all_time_top_list'])

        response = '=== AKTUELL ===\n\n'
        for index, user_id in enumerate(self.data['shit_coin_list']):
            if self.data['shit_coin_list'][user_id] > 0:
                response += f"{index + 1}. {self.id_to_nick[user_id]} mit {self.data['shit_coin_list'][user_id]} SC\n"
                
        response += '\n=== ALL-TIME ===\n\n'
        for index, user_id in enumerate(self.data['all_time_top_list']):
            if index < 5:
                response += f"{index + 1}. {self.id_to_nick[user_id]} mit {self.data['all_time_top_list'][user_id]} SC\n"
    
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Shitcoin_Users(bot))