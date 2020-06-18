import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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
    await ctx.send(f'__***' + f'ANIMATED EMOTES:' + f'***__\n\n' + animatedEmojisMessage)
    await ctx.send(f'__***' + f'EMOTES:' + f'***__\n\n' + nonAnimatedEmojisMessage)

@emojiBot.command(name='animated')
async def animated(ctx):
    emojisList = []
    for emoji in ctx.guild.emojis:
        if emoji.animated:
            emojisList.append(emojiBot.get_emoji(emoji.id))
    animatedEmojisMessage = ""
    for emoji in emojisList:
        animatedEmojisMessage += f'{emoji} ' + emoji.name + f'\n'
    await ctx.send(f'__***' + f'ANIMATED EMOTES:' + f'***__\n\n' + animatedEmojisMessage)

@emojiBot.command(name='regular')
async def regular(ctx):
    emojisList = []
    for emoji in ctx.guild.emojis:
        if emoji.animated == False:
            emojisList.append(emojiBot.get_emoji(emoji.id))
    emotesMessage = ""
    for emoji in emojisList:
        emotesMessage += f'{emoji} ' + emoji.name + f'\n'
    await ctx.send(f'__***' + f'EMOTES:' + f'***__\n\n' + emotesMessage)
emojiBot.run(TOKEN)