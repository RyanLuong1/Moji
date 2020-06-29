import os
import discord
import asyncio
import re
from dotenv import load_dotenv
from discord.ext import commands
from emojibotclass import EmojiClass
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
serverEmotes = EmojiClass()

emojiBot = commands.Bot(command_prefix = '!')

@emojiBot.event
async def on_ready():
    await emojiBot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "Ryan breaking the bot 24/7"))
# @emojiBot.command(name='get')
# async def get(ctx):
#     serverEmotes.resetBot()
#     for emoji in ctx.guild.emojis:
#         if emoji.animated:
#             serverEmotes.animatedEmotes.update( {emojiBot.get_emoji(emoji.id): 0})
#             serverEmotes.animatedEmotesMessage += f'{emoji} ' + emoji.name + f'\n'  
#         else:
#             serverEmotes.regularEmotes.update( {emojiBot.get_emoji(emoji.id): 0} )
#             serverEmotes.regularEmotesMessage += f'{emoji} ' + emoji.name + f'\n'
#     await ctx.send(f'All emotes have been updated!')

@emojiBot.command(name='emotes')
async def emotes(ctx):
    if not ctx.guild.emojis:
        await ctx.send(f'Your server does not have any custom emotes!')
    # elif serverEmotes.emotesSize == len(ctx.guild.emojis):
    #     await ctx.send(serverEmotes.animatedEmotesMessage)
    #     await ctx.send(f'\u200b\n' + serverEmotes.regularEmotesMessage)
    elif serverEmotes.emotesAmt != len(ctx.guild.emojis) and serverEmotes.emotesAmt != 0:
        dict1 = serverEmotes.animatedEmotes
        dict2 = serverEmotes.regularEmotes
        messageForAnimated = f'__***ANIMATED EMOTES:***__\n'
        messageForRegular = f'__***EMOTES:***__\n'
        serverEmotes.resetEmotes()
        for emoji in ctx.guild.emojis:
            if emoji.animated:
                serverEmotes.animatedEmotes.update( {emojiBot.get_emoji(emoji.id): 0})
                messageForAnimated += f'{emoji} ' + emoji.name + f'\n'  
            else:
                serverEmotes.regularEmotes.update( {emojiBot.get_emoji(emoji.id): 0} )
                messageForRegular += f'{emoji} ' + emoji.name + f'\n'
        for key in dict1:
            if key in serverEmotes.animatedEmotes:
                serverEmotes.animatedEmotes.update( {key: dict1[key]})
        for key in dict2:
            if key in serverEmotes.regularEmotes:
                serverEmotes.regularEmotes.update( {key: dict2[key]})
        server.emotesAmt = len(serverEmotes.animatedEmotes) + len(serverEmotes.regular)
    else:
        serverEmotes.resetEmotes()
        messageForAnimated = f'__***ANIMATED EMOTES:***__\n'
        messageForRegular = f'__***EMOTES:***__\n'
        for emoji in ctx.guild.emojis:
            if emoji.animated:
                serverEmotes.animatedEmotes.update( {emojiBot.get_emoji(emoji.id): 0})
                messageForAnimated += f'{emoji} ' + emoji.name + f'\n'
            else:
                serverEmotes.regularEmotes.update( {emojiBot.get_emoji(emoji.id): 0} )
                messageForRegular += f'{emoji} ' + emoji.name + f'\n'   
            serverEmotes.emotesAmt = len(serverEmotes.animatedEmotes) + len(serverEmotes.regularEmotes)
        await ctx.send(f'All emotes have been collected. All emotes will be display soon!')
        await asyncio.sleep(5)
        await ctx.send(messageForAnimated)
        await ctx.send(f'\u200b\n' + messageForRegular)

@emojiBot.command(name='animated')
async def animated(ctx):
    if not serverEmotes.animatedEmotes:
        await ctx.send(f'No animated emotes to display! Either you forgot to use the !emotes command or your server does not have any animated emotes.')
    else:
        message = f'__***ANIMATED EMOTES:***__\n'

        await ctx.send(serverEmotes.animatedEmotesMessage)

@emojiBot.command(name='regular')
async def regular(ctx):
    if not serverEmotes.regularEmotes:
        await ctx.send(f'No regular emotes to display! Either you forgot to use the !emotes command or your server does not have regular emotes.')
    else:
        await ctx.send(serverEmotes.regularEmotesMessage)

@emojiBot.command(name="showcounter")
async def counter(ctx):
    serverEmotes.resetMessage()
    for key in serverEmotes.animatedEmotes:
        serverEmotes.animatedEmotesCounterMessage += f'{key}' + f' ' + str(serverEmotes.animatedEmotes[key]) + f'\n'
    for key in serverEmotes.regularEmotes:
        serverEmotes.regularEmotesCounterMessage += f'{key}' + f' ' + str(serverEmotes.regularEmotes[key]) + f'\n'
    await ctx.send(serverEmotes.animatedEmotesCounterMessage)
    await ctx.send(f'\u200b\n' + serverEmotes.regularEmotesCounterMessage)

# @emojiBot.command(name='top5')
# async def showTop5(ctx):
#     top5Animated = ""
#     top5Regular = ""
#     for key in 

@emojiBot.event
async def on_message(message):
    if message.author == emojiBot.user:
        return
    emotes = re.findall(r"\<(.*?)\>", str(message.content))
    if emotes:
        for key in serverEmotes.animatedEmotes:
            if str(key.id) in message.content:
                (serverEmotes.animatedEmotes[key]) += 1
        for key in serverEmotes.regularEmotes:
            if str(key.id) in message.content:
                (serverEmotes.regularEmotes[key]) += 1
    await emojiBot.process_commands(message)


emojiBot.run(TOKEN)