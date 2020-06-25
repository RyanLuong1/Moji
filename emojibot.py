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
# @emojiBot.event
# async def on_ready():
#     my_guild = emojiBot.get_guild(168194594708652033)
#     for emoji in my_guild:
#         serverEmotes.emojiList.update( {emojiBot.get_emoji(emoji.id): 0})
#     print("here!")
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
    else:
        serverEmotes.resetEmotes()
        serverEmotes.resetMessage()
        for emoji in ctx.guild.emojis:
            if emoji.animated:
                serverEmotes.animatedEmotes.update( {emojiBot.get_emoji(emoji.id): 0})
                serverEmotes.animatedEmotesMessage += f'{emoji} ' + emoji.name + f'\n'  
            else:
                serverEmotes.regularEmotes.update( {emojiBot.get_emoji(emoji.id): 0} )
                serverEmotes.regularEmotesMessage += f'{emoji} ' + emoji.name + f'\n'
        await ctx.send(f'All emotes have been collected. All emotes will be display soon!')
        await asyncio.sleep(5)
        await ctx.send(serverEmotes.animatedEmotesMessage)
        await ctx.send(f'\u200b\n' + serverEmotes.regularEmotesMessage)

@emojiBot.command(name='animated')
async def animated(ctx):
    if not serverEmotes.animatedEmotes:
        await ctx.send(f'No animated emotes to display! Either you forgot to use the !emotes command or your server does not have any animated emotes.')
    else:
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

@emojiBot.event
async def on_message(message):
    if message.author == emojiBot.user:
        return
    # for key in serverEmotes.animatedEmotes:
    #     if key in message:
    # processedMessage = re.compile('<>')
    # if processedMessage.search(message.content) != None:
    #     for key in serverEmotes.animatedEmotes:
    #         print(key.name)
    for key in serverEmotes.animatedEmotes:
        if str(key.id) in message.content:
            (serverEmotes.animatedEmotes[key]) += 1
    for key in serverEmotes.regularEmotes:
        if str(key.id) in message.content:
            (serverEmotes.regularEmotes[key]) += 1
    await emojiBot.process_commands(message)

emojiBot.run(TOKEN)