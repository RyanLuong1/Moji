import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from emojibotclass import EmojiClass
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
serverEmotes = EmojiClass()
emojiBot = commands.Bot(command_prefix = '!')
# @emojiBot.event
# async def on_ready():
#     my_guild = emojiBot.get_guild(168194594708652033)
#     for emoji in my_guild:
#         serverEmotes.emojiList.update( {emojiBot.get_emoji(emoji.id): 0})
#     print("here!")
@emojiBot.command(name='get')
async def get(ctx):
    for emoji in ctx.guild.emojis:
        if emoji.animated:
            serverEmotes.animtedEmotes.update( {emojiBot.get_emoji(emoji.id): 0})
        else:
            serverEmotes.regularEmotes.update( {emojiBot.get_emoji(emoji.id): 0} )
    await ctx.send(f'All emotes have been updated!')

@emojiBot.command(name='emotes')
async def emotes(ctx):
    # emotesList = []
    # # emojisString = ""
    # for emoji in ctx.guild.emojis:
    #     emotesList.append(emojiBot.get_emoji(emoji.id))
    animatedEmotesMessage = ""
    regularEmotesMessage = ""
    for emoji in serverEmotes.animtedEmotes:
        animatedEmotesMessage += f'{emoji} ' + emoji.name + f'\n'
    for emoji in serverEmotes.regularEmotes:  
        regularEmotesMessage += f'{emoji} ' + emoji.name + f'\n'
    await ctx.send(f'__***' + f'ANIMATED EMOTES:' + f'***__\n' + animatedEmotesMessage)
    await ctx.send(f'\u200b\n' + f'__***' + f'EMOTES:' + f'***__\n' + regularEmotesMessage)

@emojiBot.command(name='animated')
async def animated(ctx):
    emotesList = []
    for emoji in ctx.guild.emojis:
        if emoji.animated:
            emotesList.append(emojiBot.get_emoji(emoji.id))
    animatedEmotesMessage = ""
    for emoji in emotesList:
        animatedEmotesMessage += f'{emoji} ' + emoji.name + f'\n'
    await ctx.send(f'__***' + f'ANIMATED EMOTES:' + f'***__\n' + animatedEmotesMessage)

@emojiBot.command(name='regular')
async def regular(ctx):
    emotesList = []
    for emoji in ctx.guild.emojis:
        if emoji.animated == False:
            emotesList.append(emojiBot.get_emoji(emoji.id))
    emotesMessage = ""
    for emoji in emotesList:
        emotesMessage += f'{emoji} ' + emoji.name + f'\n'
    await ctx.send(f'__***' + f'EMOTES:' + f'***__\n' + emotesMessage)
emojiBot.run(TOKEN)