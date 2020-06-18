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
    animatedEmojisMessage = ""
    nonAnimatedEmojisMessage = ""
    for emoji in emojisList:
        if emoji.animated:
            animatedEmojisMessage += f'{emoji} ' + emoji.name + f'\n'  
        else:
            nonAnimatedEmojisMessage += f'{emoji} ' + emoji.name + f'\n'
    await ctx.send(f'ANIMATED EMOTES:\n' + animatedEmojisMessage)
    await ctx.send(f'EMOTES:\n' + nonAnimatedEmojisMessage)
    # await ctx.send(animatedEmojisNames)

emojiBot.run(TOKEN)