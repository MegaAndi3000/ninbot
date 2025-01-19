import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv("NINBOT_TOKEN")

bot = commands.Bot(command_prefix='.', intents=intents)

with open("config.json", "r") as file:
    
    config = json.load(file)

@bot.event
async def on_ready():
    
    for extension in config["extension_list"]:
        await bot.load_extension(f"cogs.{extension}")

bot.run(TOKEN)