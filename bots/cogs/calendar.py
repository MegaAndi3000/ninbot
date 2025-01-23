import datetime
import json
import discord
from discord.ext import tasks, commands
from cogs.funcs.general import get_ids

timezone = datetime.timezone(datetime.timedelta(hours=1))
calendar_check_time = datetime.time(hour=0, minute=0, tzinfo=timezone)

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_check.start()

    @tasks.loop(time=calendar_check_time)
    async def daily_check(self):
        with open("Data/calendar_events.json", "r") as file:
            events = json.load(file)
            
        today = datetime.date.today().strftime("%d-%m")
        id_list = get_ids()
        channel_id = id_list["calendar"]
        channel = self.bot.get_channel(channel_id)
        
        for day, event_message in events["events"].items():
            if day == today:
                await channel.send(event_message)
                
        for day, user_id in events["birthdays"].items():
            if day == today:
                user = self.bot.get_user(user_id)
                await channel.send(f"Alles gute zum Geburtstag, {user.mention}!")

async def setup(bot):
    await bot.add_cog(Test(bot))