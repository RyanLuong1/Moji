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
    serverEmotes.resetBot()
    for emoji in ctx.guild.emojis:
        if emoji.animated:
            serverEmotes.animatedEmotes.update( {emojiBot.get_emoji(emoji.id): 0})
            serverEmotes.animatedEmotesMessage += f'{emoji} ' + emoji.name + f'\n'  
        else:
            serverEmotes.regularEmotes.update( {emojiBot.get_emoji(emoji.id): 0} )
            serverEmotes.regularEmotesMessage += f'{emoji} ' + emoji.name + f'\n'
    await ctx.send(f'All emotes have been updated!')

@emojiBot.command(name='emotes')
async def emotes(ctx):
    if not serverEmotes.animatedEmotesMessage and not serverEmotes.regularEmotesMessage:
        await ctx.send(f'Use !get command first to get all of your server emotes!')
    else:
        await ctx.send(serverEmotes.animatedEmotesMessage)
        await ctx.send(serverEmotes.regularEmotesMessage)

@emojiBot.command(name='animated')
async def animated(ctx):
    if not serverEmotes.animatedEmotesMessage:
        await ctx.send(f'No animated emotes to display!\nEither you forgot to use the !get command or your server does not have any animated emotes.')
    else:
        await ctx.send(serverEmotes.animatedEmotesMessage)

@emojiBot.command(name='regular')
async def regular(ctx):
    if not serverEmotes.regularEmotesMessage:
        await ctx.send(f'No regular emotes to display!\nEither you forgot to use the !get command or your server does not have regular emotes.')
    else:
        await ctx.send(serverEmotes.regularEmotesMessage)
emojiBot.run(TOKEN)