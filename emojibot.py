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

#TODO: Setup database
#TODO: Clean the code
#TODO: Get the percentage per page

TOKEN = os.getenv('DISCORD_TOKEN')
serverEmotes = EmojiClass()

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "Ryan breaking the bot 24/7"))

"""
(bot.get_emoji(x[0]).name).lower() -> Gets the lowercase version of the emojis names
(-x[1], (bot.get_emoji(x[0]).name)).lower())) -> Sort the dict by value in descending order then by the lowercase version of the emojis names in ascending order
Sorting the emojis by count descendingly then by name ascendingly makes the list look ordered
"""

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
        n_times = math.ceil(len(list_of_emojis) / 10)
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
        sorted_emotes = OrderedDict(sorted(serverEmotes.emojis_dict.items(), key=lambda x: (-x[1], (bot.get_emoji(x[0]).name)).lower()))
        for id, count in sorted_emotes.items():
                index = math.floor(x/10)
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
        parts = 0
        total = serverEmotes.total
        sorted_emotes = OrderedDict(sorted(serverEmotes.emojis_dict.items(), key=lambda x: (-x[1], (bot.get_emoji(x[0]).name).lower())))
        for id, count in sorted_emotes.items():
            index = math.floor(x/10)
            emoji = bot.get_emoji(id)
            parts += count
            message = f'{x+1}. {emoji}: {count}'
            serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
            x += 1
        reactionMessage = await ctx.send(embed=serverEmotes.embed_list[0]) 
        await reactionMessage.add_reaction('◀️')
        await reactionMessage.add_reaction('▶️')
    else:
        n_times = math.ceil(len(list_of_emojis) / 10)
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
        sorted_emotes = OrderedDict(sorted(serverEmotes.emojis_dict.items(), key=lambda x: (bot.get_emoji(x[0]).name).lower()))
        for id, count in sorted_emotes.items():
                index = math.floor(x/10)
                emoji = bot.get_emoji(id)
                message = f'{x+1}. {emoji}: {count}'
                serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
                x += 1
        embed_list_size = len(serverEmotes.embed_list)
        total = serverEmotes.total
        activity = 0
        for x in range(embed_list_size):
            serverEmotes.embed_list[x].description = f'Total Count: {total}\n Usage Activity: 0 ({0}%)'
        reactionMessage = await ctx.send(embed=serverEmotes.embed_list[0])
        await reactionMessage.add_reaction('◀️')
        await reactionMessage.add_reaction('▶️')

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if not reaction.message.embeds:
        id = reaction.emoji.id
        count = serverEmotes.emojis_dict.get(id, -1)
        if count != -1:
            (serverEmotes.emojis_dict[id]) += 1
    else:
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
            else:
                id = reaction.emoji.id
                count = serverEmotes.emojis_dict.get(id, -1)
                if count != -1:
                    (serverEmotes.emojis_dict[id]) += 1

"""
Discord bots write emotes as <:name_of_emotes:#>.
Parsing the message to get the emojis ids is a preferable way. 
Find the emojis ids by using the following pattern, a group of numbers that ends with a >.
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
            serverEmotes.total += 1
    await bot.process_commands(message)


bot.run(TOKEN)