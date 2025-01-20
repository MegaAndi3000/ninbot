from discord.ext import commands
from cogs.funcs.general import get_ids, get_id_to_nick

class Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def counter_message(self, message):

        with open('Data/counter.txt', 'r') as file:
            
            lines = file.readlines()
            current_counter = int(lines[0])
            last_author = lines[1]
            highscore = int(lines[2])
    
        id_list = get_ids()
        user = str(message.author.id)
        
        if message.channel.id != id_list['counter'] or message.author.id == id_list['NinBot']:
            pass
        
        else:
            try:
                
                number = int(message.content)
                
                if user == last_author:
                    await message.delete()
                    
                elif number != current_counter + 1:
                    
                    await message.delete()
                    id_to_nick = await get_id_to_nick(self.bot)
                    await message.channel.send(f"{id_to_nick[user]} hat die Streak gebrochen.")
                    current_counter = 0
                    last_author = 0
                    
                else:
                    
                    current_counter = number
                    last_author = user
                    highscore = current_counter
                    
                with open('Data/counter.txt', 'w') as file:
                    file.write(f'{current_counter}\n{last_author}\n{highscore}')
                
            except ValueError:
                await message.delete()

async def setup(bot):
    await bot.add_cog(Counter(bot))