import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

emojiBot = commands.Bot(command_prefix = '!')

@emojiBot.command(name='emojis')
async def emojis(ctx):
    emojisList = []
    # emojisString = ""
    for emoji in ctx.guild.emojis:
        emojisList.append(emojiBot.get_emoji(emoji.id))
    emojis = "";
    for emoji in emojisList:
        emojis += f'{emoji}'
    await ctx.send(emojis)

emojiBot.run(TOKEN)