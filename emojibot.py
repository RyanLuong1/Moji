import os
import discord
import asyncio
import re
import copy
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
        dict1 = {}
        dict2 = {}
        for key in serverEmotes.animatedEmotes:
            dict1.update( {key: serverEmotes.animatedEmotes[key]})
        for key in serverEmotes.regularEmotes:
            dict2.update( {key: serverEmotes.regularEmotes[key]})
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
        serverEmotes.emotesAmt = len(serverEmotes.animatedEmotes) + len(serverEmotes.regularEmotes)
        await ctx.send(f'All emotes have been collected. All emotes will be display soon!')
        await asyncio.sleep(5)
        await ctx.send(messageForAnimated)
        await ctx.send(f'\u200b\n' + messageForRegular)
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
        # await asyncio.sleep(5)
        await ctx.send(messageForAnimated)
        await ctx.send(f'\u200b\n' + messageForRegular)

@emojiBot.command(name='animated')
async def animated(ctx):
    if not serverEmotes.animatedEmotes:
        await ctx.send(f'No animated emotes to display! Either you forgot to use the !emotes command or your server does not have any animated emotes.')
    else:
        message = f'__***ANIMATED EMOTES:***__\n'
        for key in serverEmotes.animatedEmotes:
            message += f'{key}' + key.name + f'\n'
        await ctx.send(message)

@emojiBot.command(name='regular')
async def regular(ctx):
    if not serverEmotes.regularEmotes:
        await ctx.send(f'No regular emotes to display! Either you forgot to use the !emotes command or your server does not have regular emotes.')
    else:
        message = f'__***EMOTES:***__\n'
        for key in serverEmotes.regularEmotes:
            message += f'{key}' + key.name + f'\n'
        await ctx.send(message)

@emojiBot.command(name="showcounter")
async def counter(ctx):
    messageForAnimated = f'__***ANIMATED EMOTES:***__\n'
    messageForRegular = f'__***EMOTES:***__\n'
    for key in serverEmotes.animatedEmotes:
        messageForAnimated += f'{key}' + f' ' + str(serverEmotes.animatedEmotes[key]) + f'\n'
    for key in serverEmotes.regularEmotes:
        messageForRegular += f'{key}' + f' ' + str(serverEmotes.regularEmotes[key]) + f'\n'
    await ctx.send(messageForAnimated)
    await ctx.send(f'\u200b\n' + messageForRegular)

@emojiBot.command(name='top5')
async def showTop5(ctx):
    if serverEmotes.emotesAmt == 0:
        await ctx.send("You don't have any emotes. Use !emotes to get it!")
    else:
        serverEmotes.getTop5()
        top5Animated = f'__***TOP 5 ANIMATED EMOTES:***__\n'
        top5Regular = f'__***TOP 5 EMOTES:***__\n'
        for key in serverEmotes.top5AnimatedEmotes:
            top5Animated += {key} + f' ' + serverEmotes.top5AnimatedEmotes[key] + f'\n'
        for key in serverEmotes.top5RegularEmotes:
            top5Regular += {key} + f' ' + serverEmotes.top5RegularEmotes[key] + f'\n'
        await ctx.send(top5Animated)
        await ctx.send(f'\u200b\n' + top5Regular)

@emojiBot.event
async def on_message(message):
    if message.author == emojiBot.user:
        return
    # emotes = re.findall(r"\<(.*?)\>", str(message.content))
    emotesId = re.findall(r"(\d+.)\>", str(message.content))
    print(emotesId)
    for id in emotesId:
        emotes = emojiBot.get_emoji(int(id))
        if emotes != None:
            if emotes.animated:
                (serverEmotes.animatedEmotes[emotes]) += 1
            else: 
                (serverEmotes.regularEmotes[emotes]) += 1
        # for key in serverEmotes.animatedEmotes:
        #     if str(key.id) in emotes:
        #         occurrences = emotes.count(str(key.id))
        #         (serverEmotes.animatedEmotes[key]) += occurrences
        # for key in serverEmotes.regularEmotes:
        #     if str(key.id) in emotes:
        #         occurrences = emotes.count(str(key.id))
        #         (serverEmotes.regularEmotes[key]) += occurrences
    await emojiBot.process_commands(message)


emojiBot.run(TOKEN)