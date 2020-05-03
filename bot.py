# bot.py
import os
import time
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
global last_mention_timestamp
last_mention_timestamp = time.time()

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

    if message.content.lower().replace(" ","").find("pregnantclippy") >= 0:
        curr_timestamp = time.time()
        days_since_mention = int((curr_timestamp - last_mention_timestamp))
        last_mention_timestamp = curr_timestamp
        response = "It has been {n:d} seconds since pregnant clippy was last mentioned".format(n=days_since_mention)        
        await message.channel.send(response)

client.run(TOKEN)