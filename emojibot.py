import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

emojiBot = commands.Bot(command_prefix = '!')

@emojiBot.command(name='emojis')
async def emojis(ctx):
    emojisList = []
    for emoji in ctx.guild.emojis:
        emojisList.append(str(emoji.id))
    a = (" ".join(emojisList))
    await ctx.send(a)

emojiBot.run(TOKEN)