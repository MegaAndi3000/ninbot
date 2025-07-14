import os
import json
from discord.ext import commands
from cogs.funcs.general import get_ids
from cogs.funcs.shitcoin import file_load, file_update, log_event
from dotenv import load_dotenv

class Shitcoin_Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        
    async def cog_check(self, ctx):
        with open("config.json", "r") as file:
            config = json.load(file)
        return ctx.channel.id in config["sc_dev_channel_id_list"] and ctx.author.id in config["sc_dev_user_id_list"]
    
    async def cog_before_invoke(self, ctx):
        self.data = file_load()
        
    async def cog_after_invoke(self, ctx):
        file_update(self.data)
        
    @commands.command(name='add_user', help='Fügt einen neuen Nutzer hinzu.')
    async def add_user(self, ctx, user):

        self.data['shit_coin_list'][user] = 0
        self.data['daily_check_list'][user] = '1970-01-01'
        self.data['steal_check_list'][user] = 0
        self.data['all_time_top_list'][user] = 0

        log_event("add_user", {"user": user})
        await ctx.send(f'User {user} wurde hinzugefügt.')

    @commands.command(name='data_reset', help='Setzt alle Daten zurück.')
    async def data_reset(self, ctx):

        id_list = get_ids()
        guild = self.bot.get_guild(id_list['guild'])
        
        async for member in guild.fetch_members():
            if member.bot:
                pass
            user_id = str(member.id)
            self.data['shit_coin_list'][user_id] = 0 
            self.data['daily_check_list'][user_id] = '1970-01-01'
            self.data['steal_check_list'][user_id] = 0 
            self.data['all_time_top_list'][user_id] = 0 

        log_event("reset", {})
                            
    @commands.command(name = 'remove_user', help='Entfernt einen Nutzer.')
    async def remove_user(self, ctx, user):
        
        del self.data['shit_coin_list'][user], self.data['daily_check_list'][user], self.data['steal_check_list'][user], self.data['all_time_top_list'][user]
        log_event("remove_user", {"user": user})
        await ctx.send(f'User {user} wurde entfernt.')

    @commands.command(name='set', help='Setzt die SC eines Users auf einen bestimmten Wert.')
    async def coin_set(self, ctx, user, amount):

        self.data['shit_coin_list'][user] = float(amount)
        log_event("coin set", {"user": user, "amount": amount})

    @commands.command(name='show_env', help='Zeigt alle Umgebungsvariablen (.env) an.')
    async def show_env(self, ctx):

        load_dotenv(override=True)
        env_list = ['CF_PIVOT', 'DAILY_MAX', 'DAILY_MIN', 'STEAL_AMOUNT', 'STEAL_COOLDOWN', 'STEAL_COST_FACTOR', 'STEAL_PIVOT']

        response = '\n'.join([f'{variable} = {os.getenv(variable)}' for variable in env_list])
        await ctx.send(response)

    @commands.command(name='show_data', help='Zeigt alle Daten an.')
    async def show_data(self, ctx):
        
        response = ''
        for user in self.data['shit_coin_list']:
            response += f"{user}: {self.data['shit_coin_list'][user]} SC, DC {self.data['daily_check_list'][user]}, SC {self.data['steal_check_list'][user]}, T {self.data['all_time_top_list'][user]}\n"

        await ctx.channel.send(response)
        
async def setup(bot):
    await bot.add_cog(Shitcoin_Developer(bot))