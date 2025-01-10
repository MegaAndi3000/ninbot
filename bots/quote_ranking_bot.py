import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from funcs import get_ids, get_id_to_nick, sort_dic_value

load_dotenv()
TOKEN = os.getenv('NINBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def update():
    
    global author_list
    global victim_list
    
    id_list = get_ids()
    id_to_nick = await get_id_to_nick(bot)
    id_to_nick[753298872134271236] = 'Cathi'
    
    alias_list = {'Andreas': ['Andi', 'Bagehorn', 'MegaderAndi'],
                  'Templum': ['Nazi-Kon', 'Konrad T'],
                  'Tobi': ['Tobias'],
                  'Rübe': ['Konrad R'],
                  'Finn': []}
    
    channel = bot.get_channel(id_list['zitate'])
    message_list = []
    
    async for message in channel.history(limit=None):
        
        try:
            
            message_list.append({'author': id_to_nick[message.author.id],
                                'victim': message.content.split('\n-')[1].strip().split(',')[0],
                                'content': message.content.split('\n-')[0].strip('„"“'),
                                'likes': message.reactions[0].count,
                                'dislikes': message.reactions[1].count})
        
        except IndexError:
            
            pass

    del message_list[-9:]
    message_list = message_list[::-1]
    quotes_cleaned = []
    
    for quote in message_list:
        
        for name, aliases in alias_list.items():
            
            if quote['victim'].startswith(name):
                
                quote['victim'] = name
                quotes_cleaned.append(quote)

            else:
                
                for alias in aliases:
                    
                    if quote['victim'].startswith(alias):
                        
                        quote['victim'] = name
                        quotes_cleaned.append(quote)

    author_list = {}
    
    for quote in message_list:
        
        if quote['author'] not in author_list:
            
            author_list[quote['author']] = {'count': 1, 'likes': quote['likes'], 'dislikes': quote['dislikes']}
            
        else:
            
            author_list[quote['author']]['count'] += 1
            author_list[quote['author']]['likes'] += quote['likes']
            author_list[quote['author']]['dislikes'] += quote['dislikes']
   
    victim_list = {}
    
    for quote in quotes_cleaned:
        
        if quote['victim'] not in victim_list:
            
            victim_list[quote['victim']] = {'count': 1, 'likes': quote['likes'], 'dislikes': quote['dislikes']}
            
        else:
            
            victim_list[quote['victim']]['count'] += 1
            victim_list[quote['victim']]['likes'] += quote['likes']
            victim_list[quote['victim']]['dislikes'] += quote['dislikes']

@bot.event
async def on_ready():
    
    await update()
    print('Ready: quote_ranking')

@bot.command(name='zr')
async def quote_count_ranking(ctx):
    
    id_list = get_ids()
    
    if ctx.channel.id != id_list['bot-spam']:
        
        pass
    
    else:
    
        print('HERE')
    
        authors = sort_dic_value(author_list, 'count')
        victims = sort_dic_value(victim_list, 'count')

        response = '=== Autoren ===\n'
        i = 0
        
        for author, stats in authors.items():
            
            if stats['count'] >= 5:
            
                response += f'\n{i}. {author} mit {stats["count"]} Zitaten'
                i += 1
            
        response += '\n\n=== "Opfer" ===\n'
        i = 0
        
        for victim, stats in victims.items():
            
            response += f'\n{i}. {victim} mit {stats["count"]} Zitaten'
            i += 1
            
        await ctx.send(response)
        
bot.run(TOKEN)