# bot.py
import os
from os import path
import time
import string
import discord
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

def handle_mention(message):
    global last_mention_timestamp
    if message.author == client.user:
        return
    cleaned_msg = message.content.lower().replace(" ","")
    if list_find(cleaned_msg):
        curr_timestamp = time.time()
        print("current")
        print(curr_timestamp)
        print("last")
        print(last_mention_timestamp)
        days_since_mention = int((curr_timestamp - last_mention_timestamp))
        last_mention_timestamp = curr_timestamp
        save_streak()
        response = "Pregnant clippy was last mentioned {n:d} seconds before now".format(n=days_since_mention)        
        return response

@client.event
async def on_message(message):
    response = handle_mention(message)
    if response:
        await message.channel.send(response)

@client.event
async def on_message_edit(message_before, message_after):
    response = handle_mention(message_after)
    if response:
        await message_after.channel.send(response)

@client.event
async def on_disconnect():
    save_streak()

client.run(TOKEN)
