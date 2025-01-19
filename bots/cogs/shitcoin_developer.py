import os
from discord.ext import commands
from cogs.funcs.general import get_ids, get_id_to_nick, get_nick_to_id
from cogs.funcs.shitcoin import file_load, update

class Shitcoin_Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='add_user', help='DEBUG: Fügt einen neuen Nutzer hinzu.')
    async def add_user(self, ctx, target):

        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return
        elif ctx.author.id != id_list['MegaAndi3000']:
            await ctx.send('Du bist dazu nicht berechtigt. Sorry!')
            return
            
        user = int(target)
        
        shit_coin_list[user] = 0
        daily_check_list[user] = '1970-01-01'
        steal_check_list[user] = 0
        all_time_top_list[user] = 0
        
        update(shit_coin_list, daily_check_list, steal_check_list, all_time_top_list)
        await ctx.send(f'User {int(target)} wurde hinzugefügt.')

    @commands.command(name='data_reset', help='DEBUG: Setzt alle Daten zurück.')
    async def data_reset(self, ctx):
        
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return
        elif ctx.author.id != id_list['MegaAndi3000']:
            await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
            return
    
        with open('Data/shitcoin.txt', 'w') as file:
            for guild in self.bot.guilds:
                if guild.id == id_list['guild']:
                    async for member in guild.fetch_members():
                        if member.bot == False:
                            file.write(f'{member.id}@0@1970-01-01@0@0\n')
                            
    @commands.command(name = 'remove_user', help='DEBUG: Entfernt einen Nutzer.')
    async def remove_user(self, ctx, target):
        
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return
        elif ctx.author.id != id_list['MegaAndi3000']:
            await ctx.send('Du bist dazu nicht berechtigt. Sorry!')
            return

        user = int(target)        
        del shit_coin_list[user], daily_check_list[user], steal_check_list[user], all_time_top_list[user]
        
        update(shit_coin_list, daily_check_list, steal_check_list, all_time_top_list)
        await ctx.send(f'User {user} wurde entfernt.')

    @commands.command(name='set', help='DEBUG: Setzt die SC eines Users auf einen bestimmten Wert.')
    async def coin_set(self, ctx, user, amount):
                
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return
        elif ctx.author.id != id_list['MegaAndi3000']:
            await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
            return

        shit_coin_list[int(user)] = int(amount)
            
        update(shit_coin_list, daily_check_list, steal_check_list, all_time_top_list)

    @commands.command(name='show_env', help='DEBUG: Zeigt alle Umgebungsvariablen (.env) an.')
    async def show_env(self, ctx):
        
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return
        elif ctx.author.id != id_list['MegaAndi3000']:
            await ctx.send('Du bist dazu nicht berechtigt. Sorry!')
            return

        update()
        env_list = ['CF_PIVOT', 'DAILY_MAX', 'DAILY_MIN', 'STEAL_AMOUNT', 'STEAL_COOLDOWN', 'STEAL_COST_FACTOR', 'STEAL_PIVOT']

        response = ''
        for variable in env_list:
            response += f'{variable} = {os.getenv(variable)}\n'
        
        await ctx.send(response)

    @commands.command(name='show_data', help='DEBUG: Zeigt alle Daten an.')
    async def show_data(self, ctx):
                
        shit_coin_list, daily_check_list, steal_check_list, all_time_top_list = file_load()
        id_list = get_ids()
        
        if ctx.channel.id != id_list['shitcoin']:
            return
        elif ctx.author.id != id_list['MegaAndi3000']:
            await ctx.channel.send('Du bist dazu nicht berechtigt. Sorry!')
            return
        
        response = ''
        for user in shit_coin_list:
            response += f'{user}: {shit_coin_list[user]} SC, DC {daily_check_list[user]}, SC {steal_check_list[user]}, T {all_time_top_list[user]}\n'

        await ctx.channel.send(response)
        
async def setup(bot):
    await bot.add_cog(Shitcoin_Developer(bot))