import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')

extensions = ['cogs.CommandEvents', 'cogs.EmoteCommand']
if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)
bot.run(TOKEN)