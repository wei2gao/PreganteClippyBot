# bot.py
import os
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
    last_mention_timestamp = time.time()
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    global last_mention_timestamp
    if message.author == client.user:
        return
    cleaned_msg = message.content.lower().replace(" ","")
    if list_find(cleaned_msg):
        curr_timestamp = time.time()
        days_since_mention = int((curr_timestamp - last_mention_timestamp))
        last_mention_timestamp = curr_timestamp
        response = "Pregnant clippy was last mentioned {n:d}} seconds before now".format(n=days_since_mention)        
        await message.channel.send(response)

client.run(TOKEN)