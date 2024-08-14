import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from funcs import get_ids, get_id_to_nick

load_dotenv()
TOKEN = os.getenv('NINBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    
    print('READY')
       
    id_list = get_ids()
    id_to_nick = await get_id_to_nick(bot)
    id_to_nick[753298872134271236] = 'Cathi'
    
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
    
    print('Done')
    
    # unique_victims = []
    
    # for quote in message_list:
        
    #     if quote['victim'] not in unique_victims:
            
    #         unique_victims.append(quote['victim'])
            
    # print(unique_victims)

    alias_list = {'Andreas': ['Andi', 'Bagehorn', 'MegaderAndi'],
                  'Templum': ['Konrad', 'Nazi-Kon'],
                  'Tobi': ['Tobias'],
                  'Rübe': [],
                  'Finn': []}
    
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
            
    # for author, stats in author_list.items():
        
    #     print(f'{author}: {stats['count']} Zitate, {stats['likes']} Likes, {stats['dislikes']} Dislikes, {stats['likes']/stats['count']:.2f} DLikes, {stats['dislikes']/stats['count']:.2f} DDislikes')

    victim_list = {}
    
    for quote in quotes_cleaned:
        
        if quote['victim'] not in victim_list:
            
            victim_list[quote['victim']] = {'count': 1, 'likes': quote['likes'], 'dislikes': quote['dislikes']}
            
        else:
            
            victim_list[quote['victim']]['count'] += 1
            victim_list[quote['victim']]['likes'] += quote['likes']
            victim_list[quote['victim']]['dislikes'] += quote['dislikes']

    for victim, stats in victim_list.items():

        print(f'{victim}: {stats['count']} Zitate, {stats['likes']} Likes, {stats['dislikes']} Dislikes, {stats['likes']/stats['count']:.2f} DLikes, {stats['dislikes']/stats['count']:.2f} DDislikes')

    max_likes_list = []
    max_likes = 0
    
    max_dislikes_list = []
    max_dislikes = 0

    for quote in message_list:
        
        if quote['likes'] > max_likes:
            
            max_likes = quote['likes']
            max_likes_list = [quote]
            
        elif quote['likes'] == max_likes:
            
            max_likes_list.append(quote)
            
        if quote['dislikes'] > max_dislikes:
            
            max_dislikes = quote['dislikes']
            max_dislikes_list = [quote]
            
        elif quote['dislikes'] == max_dislikes:
            
            max_dislikes_list.append(quote)
            
    # print(f'LIKES\n\n{max_likes_list}\n\nDISLIKES\n\n{max_dislikes_list}')

bot.run(TOKEN)