import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()

#TODO: Setup database
#TODO: Clean the code
#TODO: Right now, there's two seperate classes for the cogs. Find a way to have a single variable for both cogs

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')

# @bot.event
# async def on_ready():
#     await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "Ryan breaking the bot 24/7"))

extensions = ['cogs.CommandEvents', 'cogs.EmoteCommand']
if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)
bot.run(TOKEN)