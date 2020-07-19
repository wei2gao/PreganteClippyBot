# bot.py
import os
from os import path
import time
import string
import discord
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
global last_mention_timestamp
last_mention_timestamp = time.time()

triggerwords = []

streak_filename = ".pretnetclippy"

def save_streak():
    global last_mention_timestamp
    print(last_mention_timestamp)
    with open(streak_filename, 'w') as savefile:
        savefile.write(str(last_mention_timestamp))
        
def load_streak():
    global last_mention_timestamp
    with open(streak_filename, 'r') as savefile:
        lines = savefile.readlines()
        for line in lines:
            last_mention_timestamp = float(line.rstrip())

    
file = open("prangent.txt","r")
for line in file:
    triggerwords.append(line.rstrip())

file.close()
print(triggerwords)

def list_find(word):
    for w in triggerwords:
        if w in word:
            return True
    return False

@client.event
async def on_ready():
    global last_mention_timestamp
    if path.exists(streak_filename):
        load_streak()
    else:
        last_mention_timestamp = time.time()

    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

def convert_seconds(seconds):
    sec = seconds
    # return a string saying "x days, x minutes,", etc.
    sec_per_day = 60*60*24
    sec_per_hour = 60*60
    sec_per_minute = 60

    days = sec // sec_per_day
    sec = sec - days*sec_per_day
    hours = sec // sec_per_hour
    sec = sec - hours*sec_per_hour
    minutes = sec // sec_per_minute
    sec = sec - minutes*sec_per_minute
    time_str = "{n1:d} days, {n2:d} hours, {n3:d} minutes, and {n4:d} seconds".format(n1=days,n2=hours,n3=minutes,n4=sec)
    return time_str

def handle_mention(message):
    global last_mention_timestamp
    if message.author == client.user:
        return
    cleaned_msg = message.content.lower().replace(" ","") 
    emoji_mention = (":clippy:" in cleaned_msg or ":clippyplane:" in cleaned_msg) and "🤰" in cleaned_msg

    if list_find(cleaned_msg) or emoji_mention:
        curr_timestamp = time.time()
        print("current")
        print(curr_timestamp)
        print("last")
        print(last_mention_timestamp)
        sec_since_mention = int((curr_timestamp - last_mention_timestamp))
        last_mention_timestamp = curr_timestamp
        save_streak()
        response = "Pregnant clippy was last mentioned {n:s} before now".format(n=convert_seconds(sec_since_mention))        
        return response

@client.event
async def on_message(message):
    response = handle_mention(message)
    if response:
        await message.channel.send(response)
    else:
        # See if the message contains :clippy: or :clippyplane:
        if message.author == client.user:
            return
        cleaned_msg = message.content
        if ":clippy:" in cleaned_msg:
            emoji = client.get_emoji(709226943135875073)
            await message.add_reaction( emoji)
        elif ":clippyplane:" in cleaned_msg:
            emoji = client.get_emoji(709227225102286889)
            await message.add_reaction(emoji)

        

@client.event
async def on_message_edit(message_before, message_after):
    response = handle_mention(message_after)
    if response:
        await message_after.channel.send(response)

@client.event
async def on_disconnect():
    save_streak()

client.run(TOKEN)
