import os, sys
import json
import time
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
    
@bot.event
async def on_command_error(ctx, error): # Errors occuring in command, e.g. in .cf
    print(str(int(time.time())), '~', error)
    if not isinstance(error, commands.errors.CommandNotFound) and not isinstance(error, commands.CheckFailure):
        with open("Logs/errors.txt", "a") as file:
            file.write(" ~ ".join([str(int(time.time())), str(ctx.channel.id), str(ctx.author.id), ctx.message.content, str(error)]) + "\n")

@bot.event
async def on_error(event, ctx): # Errors not occuring in commands, e.g. in log_message
    print(str(int(time.time())), '~', sys.exc_info()[1])
    with open("Logs/errors.txt", "a") as file:
        file.write(" ~ ".join([str(int(time.time())), str(ctx.channel.id), str(ctx.author.id), str(ctx.content), str(sys.exc_info()[1])]) + "\n")

bot.run(TOKEN)