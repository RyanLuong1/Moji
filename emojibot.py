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

#TODO: Make reactions count towards the emotes

TOKEN = os.getenv('DISCORD_TOKEN')
serverEmotes = EmojiClass()

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "Ryan breaking the bot 24/7"))

@bot.command(name='emotes')
async def emotes(ctx):
    list_of_emojis = ctx.guild.emojis
    if not list_of_emojis:
        await ctx.send(f'Your server does not have any custom emotes!')
    elif len(serverEmotes.emojis_dict) != len(list_of_emojis) and len(serverEmotes.emojis_dict) != 0:
        list_of_removed_emojis = []
        for id in serverEmotes.emojis_dict:
            emoji = bot.get_emoji(id)
            if emoji == None:
                list_of_removed_emojis.append(id)
        if list_of_removed_emojis:
            for id in list_of_removed_emojis:
                del serverEmotes.emojis_dict[id]
        for emoji in list_of_emojis:
            count = serverEmotes.emojis_dict.get(emoji.id, -1)
            if count == -1:
                serverEmotes.emojis_dict.update({emoji.id: 0})
        serverEmotes.embed_list.clear()
        n_times = math.ceil(len(list_of_emojis) / 20)
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
        sorted_emotes = OrderedDict(sorted(serverEmotes.emojis_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))
        for id, count in sorted_emotes.items():
                index = math.floor(x/20)
                emoji = bot.get_emoji(id)
                message = f'{x+1}. {emoji}: {count}'
                serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
                x += 1
        reactionMessage = await ctx.send(embed=serverEmotes.embed_list[0])
        await reactionMessage.add_reaction('◀️')
        await reactionMessage.add_reaction('▶️')
    elif len(serverEmotes.emojis_dict) == len(list_of_emojis):
        list_of_removed_emojis = []
        for id in serverEmotes.emojis_dict:
            emoji = bot.get_emoji(id)
            if emoji == None:
                list_of_removed_emojis.append(id)
        if list_of_removed_emojis:
            for id in list_of_removed_emojis:
                del serverEmotes.emojis_dict[id]
        for emoji in list_of_emojis:
            count = serverEmotes.emojis_dict.get(emoji.id, -1)
            if count == -1:
                serverEmotes.emojis_dict.update({emoji.id: 0})
        for embeds in serverEmotes.embed_list:
            embeds.clear_fields()
        x = 0
        sorted_emotes = OrderedDict(sorted(serverEmotes.emojis_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))
        for id, count in sorted_emotes.items():
            index = math.floor(x/20)
            emoji = bot.get_emoji(id)
            message = f'{x+1}. {emoji}: {count}'
            serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
            x += 1
        reactionMessage = await ctx.send(embed=serverEmotes.embed_list[0]) 
        await reactionMessage.add_reaction('◀️')
        await reactionMessage.add_reaction('▶️')
    else:
        n_times = math.ceil(len(list_of_emojis) / 20)
        for x in range(n_times):
            embed = discord.Embed(
            title = "Emotes",
            description = "",
            colour = discord.Colour.blue()
            )
            pg_num = f'Page {x+1}/{n_times}'
            embed.set_footer(text=pg_num)
            serverEmotes.embed_list.append(embed)
        for emoji in list_of_emojis:
            serverEmotes.emojis_dict.update({emoji.id: 0})
        x = 0
        sorted_emotes = OrderedDict(sorted(serverEmotes.emojis_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))
        for id, count in sorted_emotes.items():
                index = math.floor(x/20)
                emoji = bot.get_emoji(id)
                message = f'{x+1}. {emoji}: {count}'
                serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
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
    #     for id in serverEmotes.animatedEmotes:
    #         dict1.update( {id: serverEmotes.animatedEmotes[id]})
    #     for id in serverEmotes.regularEmotes:
    #         dict2.update( {id: serverEmotes.regularEmotes[id]})
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
    #     for id in dict1:
    #         if id in serverEmotes.animatedEmotes:
    #             serverEmotes.animatedEmotes.update( {id: dict1[id]})
    #     for id in dict2:
    #         if id in serverEmotes.regularEmotes:
    #             serverEmotes.regularEmotes.update( {id: dict2[id]})
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
    list_of_ids = re.findall(r"(\d+.)\>", str(message.content))
    for id in list_of_ids:
        emoji = bot.get_emoji(int(id))
        if emoji != None:
            (serverEmotes.emojis_dict[int(id)]) += 1
        # for id in serverEmotes.animatedEmotes:
        #     if str(id.id) in emotes:
        #         occurrences = emotes.count(str(id.id))
        #         (serverEmotes.animatedEmotes[id]) += occurrences
        # for id in serverEmotes.regularEmotes:
        #     if str(id.id) in emotes:
        #         occurrences = emotes.count(str(id.id))
        #         (serverEmotes.regularEmotes[id]) += occurrences
    await bot.process_commands(message)


bot.run(TOKEN)