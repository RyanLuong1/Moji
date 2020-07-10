import os
import discord
import asyncio
import re
import math
from collections import OrderedDict
from dotenv import load_dotenv
from discord.ext import commands
from emojibotclass import EmojiClass
load_dotenv()

#TODO: Sort the dict by values

TOKEN = os.getenv('DISCORD_TOKEN')
serverEmotes = EmojiClass()

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "Ryan breaking the bot 24/7"))

@bot.command(name='emotes')
async def emotes(ctx):
    list_of_emotes = ctx.guild.emojis
    if not list_of_emotes:
        await ctx.send(f'Your server does not have any custom emotes!')
    elif len(serverEmotes.emotes_dict) != len(list_of_emotes) and len(serverEmotes.emotes_dict) != 0:
        list_of_removed_emotes = []
        for key,value in serverEmotes.emotes_dict.items():
            emoji = bot.get_emoji(key)
            if emoji == None:
                list_of_removed_emotes.append(key)
        for id in list_of_removed_emotes:
            del serverEmotes.emotes_dict[id]
        for emojis in list_of_emotes:
            if emojis.id not in serverEmotes.emotes_dict:
                serverEmotes.emotes_dict.update({emojis.id: 0})
        serverEmotes.embed_list.clear()
        n_times = math.ceil(len(list_of_emotes) / 20)
        for x in range(n_times):
            embed = discord.Embed(
            title = "Emotes",
            description = "",
            colour = discord.Colour.blue()
            )
            pg_num = f'Page {x+1}/{n_times}'
            embed.set_footer(text=pg_num)
            serverEmotes.embed_list.append(embed)
        x = 0
        sorted_emotes = OrderedDict(sorted(serverEmotes.emotes_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))
        for key, value in sorted_emotes.items():
                index = math.floor(x/20)
                emojis = bot.get_emoji(key)
                message = f'{x+1}. {emojis}: {value}'
                serverEmotes.embed_list[index].add_field(name=emojis.name, value=message, inline=False)
                x += 1
        reactionMessage = await ctx.send(embed=serverEmotes.embed_list[0])
        await reactionMessage.add_reaction('◀️')
        await reactionMessage.add_reaction('▶️')
    elif len(serverEmotes.emotes_dict) == len(list_of_emotes):
        isTheSame = True
        list_of_removed_emotes = []
        for key,value in serverEmotes.emotes_dict.items():
            emoji = bot.get_emoji(key)
            if emoji == None:
                list_of_removed_emotes.append(key)
                isTheSame = False
        if isTheSame == False:
            for id in list_of_removed_emotes:
                del serverEmotes.emotes_dict[id]
            for emojis in list_of_emotes:
                if emojis.id not in serverEmotes.emotes_dict:
                    serverEmotes.emotes_dict.update({emojis.id: 0})
        for embeds in serverEmotes.embed_list:
            embeds.clear_fields()
        x = 0
        sorted_emotes = OrderedDict(sorted(serverEmotes.emotes_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))
        for key, value in sorted_emotes.items():
            index = math.floor(x/20)
            emojis = bot.get_emoji(key)
            message = f'{x+1}. {emojis}: {value}'
            serverEmotes.embed_list[index].add_field(name=emojis.name, value=message, inline=False)
            x += 1
        reactionMessage = await ctx.send(embed=serverEmotes.embed_list[0]) 
        await reactionMessage.add_reaction('◀️')
        await reactionMessage.add_reaction('▶️')
    else:
        n_times = math.ceil(len(list_of_emotes) / 20)
        for x in range(n_times):
            embed = discord.Embed(
            title = "Emotes",
            description = "",
            colour = discord.Colour.blue()
            )
            pg_num = f'Page {x+1}/{n_times}'
            embed.set_footer(text=pg_num)
            serverEmotes.embed_list.append(embed)
        for emojis in list_of_emotes:
            serverEmotes.emotes_dict.update({emojis.id: 0})
        x = 0
        sorted_emotes = OrderedDict(sorted(serverEmotes.emotes_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))
        for key, value in sorted_emotes.items():
                index = math.floor(x/20)
                emojis = bot.get_emoji(key)
                message = f'{x+1}. {emojis}: {value}'
                serverEmotes.embed_list[index].add_field(name=emojis.name, value=message, inline=False)
                x += 1
        reactionMessage = await ctx.send(embed=serverEmotes.embed_list[0])
        await reactionMessage.add_reaction('◀️')
        await reactionMessage.add_reaction('▶️')
    # await ctx.send_message(channel, embed=embed)
    # # elif serverEmotes.emotesSize == len(ctx.guild.emojis):
    # #     await ctx.send(serverEmotes.animatedEmotesMessage)
    # #     await ctx.send(f'\u200b\n' + serverEmotes.regularEmotesMessage)
    # elif serverEmotes.emotesAmt != len(ctx.guild.emojis) and serverEmotes.emotesAmt != 0:
    #     dict1 = {}
    #     dict2 = {}
    #     for key in serverEmotes.animatedEmotes:
    #         dict1.update( {key: serverEmotes.animatedEmotes[key]})
    #     for key in serverEmotes.regularEmotes:
    #         dict2.update( {key: serverEmotes.regularEmotes[key]})
    #     messageForAnimated = f'```__***ANIMATED EMOTES:***__\n```'
    #     messageForRegular = f'```__***EMOTES:***__\n```'
    #     serverEmotes.resetEmotes()
    #     for emoji in ctx.guild.emojis:
    #         if emoji.animated:
    #             serverEmotes.animatedEmotes.update( {bot.get_emoji(emoji.id): 0})
    #             messageForAnimated += f'{emoji} ' + emoji.name + f'\n'  
    #         else:
    #             serverEmotes.regularEmotes.update( {bot.get_emoji(emoji.id): 0} )
    #             messageForRegular += f'{emoji} ' + emoji.name + f'\n'
    #     for key in dict1:
    #         if key in serverEmotes.animatedEmotes:
    #             serverEmotes.animatedEmotes.update( {key: dict1[key]})
    #     for key in dict2:
    #         if key in serverEmotes.regularEmotes:
    #             serverEmotes.regularEmotes.update( {key: dict2[key]})
    #     serverEmotes.emotesAmt = len(serverEmotes.animatedEmotes) + len(serverEmotes.regularEmotes)
    #     await ctx.send(f'All emotes have been collected. All emotes will be display soon!')
    #     await asyncio.sleep(5)
    #     await ctx.send(messageForAnimated)
    #     await ctx.send(f'\u200b\n' + messageForRegular)
    # else:
    #     serverEmotes.resetEmotes()
    #     messageForAnimated = f'```__***ANIMATED EMOTES:***__\n```'
    #     messageForRegular = f'```__***EMOTES:***__\n```'
    #     for emoji in ctx.guild.emojis:
    #         if emoji.animated:
    #             serverEmotes.animatedEmotes.update( {bot.get_emoji(emoji.id): 0})
    #             messageForAnimated += f'{emoji} ' + emoji.name + f'\n'
    #         else:
    #             serverEmotes.regularEmotes.update( {bot.get_emoji(emoji.id): 0} )
    #             messageForRegular += f'{emoji} ' + emoji.name + f'\n'   
    #         serverEmotes.emotesAmt = len(serverEmotes.animatedEmotes) + len(serverEmotes.regularEmotes)
    #     await ctx.send(f'All emotes have been collected. All emotes will be display soon!')
    #     # await asyncio.sleep(5)
    #     await ctx.send(messageForAnimated)
    #     await ctx.send(f'\u200b\n' + messageForRegular)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.message.embeds[0].title == "Emotes":
        if reaction.emoji == '◀️':
            if serverEmotes.pg_num == 0:
                serverEmotes.pg_num = len(serverEmotes.embed_list) - 1
                pg_num = serverEmotes.pg_num
                embed = serverEmotes.embed_list[pg_num]
                await reaction.message.edit(embed=embed)
            else:
                serverEmotes.pg_num -= 1
                pg_num = serverEmotes.pg_num
                embed = serverEmotes.embed_list[pg_num]
                await reaction.message.edit(embed=embed)
            await reaction.remove(user)
        elif reaction.emoji == '▶️':
            if serverEmotes.pg_num == len(serverEmotes.embed_list) - 1:
                serverEmotes.pg_num = 0
                pg_num = serverEmotes.pg_num
                embed = serverEmotes.embed_list[pg_num]
                await reaction.message.edit(embed=embed)
            else:
                serverEmotes.pg_num += 1
                pg_num = serverEmotes.pg_num
                embed = serverEmotes.embed_list[pg_num]
                await reaction.message.edit(embed=embed)
            await reaction.remove(user)

"""
Discord bots write emotes as <:name_of_emotes:#>. 
finall gets all the strings from the message that follow this pattern, #>, and then removing > at the end.
"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    emotesId = re.findall(r"(\d+.)\>", str(message.content))
    for id in emotesId:
        emotes = bot.get_emoji(int(id))
        if emotes != None:
            (serverEmotes.emotes_dict[int(id)]) += 1
        # for key in serverEmotes.animatedEmotes:
        #     if str(key.id) in emotes:
        #         occurrences = emotes.count(str(key.id))
        #         (serverEmotes.animatedEmotes[key]) += occurrences
        # for key in serverEmotes.regularEmotes:
        #     if str(key.id) in emotes:
        #         occurrences = emotes.count(str(key.id))
        #         (serverEmotes.regularEmotes[key]) += occurrences
    await bot.process_commands(message)


bot.run(TOKEN)