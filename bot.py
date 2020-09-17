# bot.py
import os

import discord
from dotenv import load_dotenv
from random import randrange

load_dotenv(verbose=True)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    if not guild:
        print(f'Guild {GUILD} not found! Exiting.')
        exit(0)

    members = [member.name for member in guild.members]
    
    print(f'{client.user} is connected to {guild.name} (id: {guild.id})')
    print('Members:\n' + '\n'.join(members))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'f':
        filename = f'assets/f{randrange(1, 6)}.jpg'
        print(filename)
        await message.channel.send(file=discord.File(filename))

    if message.content.lower() == 'sasuke':
        filename = 'assets/sfw_sasuke.jpg'
        print(filename)
        await message.channel.send(file=discord.File(filename))

client.run(TOKEN)