import time
from discord.ext import commands

class Message_Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def log_message(self, message):
        with open(f'Logs/{message.channel.id}.txt', 'a') as file:
            file.write(f'\n~ {int(time.mktime(message.created_at.timetuple()))} ~ {message.id} ~ {message.author.id} ~ {message.content}')

    @commands.Cog.listener("on_raw_message_edit")
    async def log_edit(self, event):
        with open('Logs/edits.txt', 'a') as file:
            file.write(f'\n~ {int(time.mktime(time.strptime(event.data["edited_timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")))} ~ {event.channel_id} ~ {event.message_id} ~ {event.data["author"]["id"]} ~ {event.data["content"]}')

    @commands.Cog.listener("on_raw_message_delete")
    async def log_deletion(self, event):
        with open('Logs/deletions.txt', 'a') as file:
            file.write(f'\n~ {int(time.time())} ~ {event.channel_id} ~ {event.message_id}')
            
async def setup(bot):
    await bot.add_cog(Message_Log(bot))