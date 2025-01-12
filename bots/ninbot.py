import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv("NINBOT_TOKEN")

bot = commands.Bot(command_prefix='.', intents=intents)

extension_list = []

@bot.event
async def on_ready():
    
    for extension in extension_list:
        await bot.load_extension(f"cogs.{extension}")

bot.run(TOKEN)