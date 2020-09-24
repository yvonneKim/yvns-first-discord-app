# bot.py
import os

import discord
import requests
import shutil
import sys
from random import randrange
from json import load, dumps

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

db = {}

@client.event
async def on_ready():
    print(f'Token is {TOKEN}')
    guild = discord.utils.get(client.guilds, name=GUILD)
    if not guild:
        print(f'Guild {GUILD} not found! Exiting.')
        exit(0)

    print(f'Guild {GUILD} found!')

    load_img_db()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = message.content.lower()
    if command.startswith('add:'):
        key = command.split(':')[-1]
        print(f'Adding {key}')
        sys.stdout.flush()
        filename = message.attachments[0].filename
        url = message.attachments[0].url

        download(url, filename)
        db[key] = db.get(key, []) + [filename]
        save_img_db()

    if command in db:
        images = db[command]
        img_filename = images[randrange(0, len(images))]
        print(f'Received command {command}')
        sys.stdout.flush()
        await message.channel.send(file=discord.File('assets/'+img_filename))

def download(url, filename):
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

    with open('assets/'+filename,'wb') as f:
        shutil.copyfileobj(r.raw, f)

def load_img_db():
    with open('img_db.json', 'r') as inf:
        global db
        db = load(inf)

def save_img_db():
    with open('img_db.json', 'w') as outf:
        global db
        outf.write(dumps(db, indent=4))

client.run(TOKEN)