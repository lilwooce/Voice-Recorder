import discord
import os
import sys
import traceback
import requests
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from discord.ext.audiorec import NativeVoiceClient  # important!
import random
import stripe 
from time import sleep

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
updatePURL = os.getenv('UP_URL')
addPrefix = os.getenv('AP_URL')
removePURL = os.getenv('RP_URL')
getPURL = os.getenv('GP_URL')
updatePremium = os.getenv('upPremium')
addPremium = os.getenv('addPremium')
getPremium = os.getenv('getPremium')

intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)
header = {"User-Agent": "XY"}

def get_prefix(client, message):
    obj = {"f1": "server", "q1": message.guild.id}
    result = requests.get(getPURL, params=obj, headers={"User-Agent": "XY"})
    prefix = result.text.strip('\"')
    return prefix

initial_extensions = {
    "cogs.Config",
    "cogs.Voice"
}

def exists(id):
    result = requests.get(getPremium, params={"f1": "userID", "f2": id}, headers=header)
    n = result.text.replace('"', '')
    print(f"got {n} from database")
    print(f"users id is {id} as a parameter")
    if (id == n):
        return True
    else:
        return False

def addUser(id):
    r = requests.post(addPremium, data={"f1": id}, headers={"User-Agent": "XY"})

def roleCheck(guild):
    if get(guild.roles, name="Premium"):
        return True
    else:
        return False

@bot.event
async def on_guild_join(guild):
    botMember = await guild.get_member(bot.user.id)
    botRole = botMember.roles[0]
    botRole.edit(position=0)
    print("moved bot pos")

    obj = {"f1": guild.id, "f2": '!'}
    result = requests.post(addPrefix, data=obj, headers={"User-Agent": "XY"})
    if(not roleCheck(guild)):
        premRole = await guild.create_role(name="Premium", colour=discord.Colour(00000000))
        totalRoles = len(guild.roles)
        await premRole.edit(position=totalRoles+1)

    role = get(guild.roles, name="Premium")
    for member in guild.members:
        if(member.bot):
            print("this is a bot")
            continue
        print("this is not a bot")

        if (not exists(member.id)):
            addUser(member.id)

        premStatus = requests.get(getPremium, params={"f1": "isPremium", "f2": member.id, "f3": "userID"}, headers=header)
        premStatus = premStatus.text.replace('"', '')
        if ((not role in member.roles) and (premStatus == "0")):
            await member.add_roles(role)

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
