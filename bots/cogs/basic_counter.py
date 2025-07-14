from discord.ext import commands
from cogs.funcs.general import get_ids

class Basic_Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def basic_counter_message(self, message):

        id_list = get_ids()
        if message.channel.id != id_list['basic-counter']:
            return

        with open('Data/basic_counter.txt', 'r') as file:
            lines = file.readlines()
            current_counter = int(lines[0])
            last_author = int(lines[1])

        try:
            number = int(message.content)
        except ValueError:
            await message.delete()
            return

        if message.author.id == last_author or number != current_counter + 1:
            await message.delete()
        else:
            current_counter = number
            last_author = message.author.id
            with open('Data/basic_counter.txt', 'w') as file:
                file.write(f'{current_counter}\n{last_author}')

async def setup(bot):
    await bot.add_cog(Basic_Counter(bot))