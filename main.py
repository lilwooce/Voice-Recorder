import discord
import os
import sys
import traceback
import requests
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.audiorec import NativeVoiceClient  # important!
import random
import stripe 
from time import sleep

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
updatePURL = os.getenv('UP_URL')
removePURL = os.getenv('RP_URL')
getPURL = os.getenv('GP_URL')
updatePremium = os.getenv('upPremium')
addPremium = os.getenv('addPremium')

intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)

def get_prefix(client, message):
    obj = {"f1": "server", "q1": message.guild.id}
    result = requests.get(getPURL, params=obj, headers={"User-Agent": "XY"})
    prefix = result.text.strip('\"')
    return prefix

initial_extensions = {
    "cogs.Config",
    "cogs.Voice"
}

@bot.event
async def on_guild_join(guild):
    obj = {"f1": guild.id, "q1": '!'}
    result = requests.post(updatePURL, data=obj, headers={"User-Agent": "XY"})
    for member in guild.members:
            requests.post(addPremium, data={"f1": member.id}, headers={"User-Agent": "XY"})
    print(result.status_code)

@bot.event
async def on_guild_remove(guild):
    obj = {"q1": guild.id}
    result = requests.post(removePURL, data=obj, headers={"User-Agent": "XY"})
    print(result.status_code)


for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}.', file=sys.stderr)
        traceback.print_exc()

bot.run(token)
