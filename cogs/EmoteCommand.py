from discord.ext import commands
from collections import OrderedDict
from emojibotclass import EmojiClass
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import math
import discord
load_dotenv()

mongo_url = os.getenv('CONNECTION_URL')
cluster = MongoClient(mongo_url)
db = cluster['emotes']
collection = db['emotes']

#TODO: Emotes are inserted 0-8 instead of 0-9

class EmoteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def reset_database():
        collection.remove({})

    def insert_emojis_to_database(emoji_id):
        query = {"_id": emoji_id}
        if (collection.count_documents(query) == 0):
                entry = {"_id": emoji_id, "count": 0}
                collection.insert_one(entry)
    """
    (bot.get_emoji(x[0]).name).lower() -> Gets the lowercase version of the emojis names
    (-x[1], (bot.get_emoji(x[0]).name)).lower())) -> Sort the dict by value in descending order then by the lowercase version of the emojis names in ascending order
    Sorting the emojis by count descendingly then by name ascendingly makes the list look ordered
    """

    @commands.command(name='emotes')
    async def emotes(self ,ctx):
        list_of_emojis = ctx.guild.emojis
        if not list_of_emojis:
            await ctx.send(f'Your server does not have any custom emotes!')
        else:
            for emoji in list_of_emojis:
                EmoteCommand.insert_emojis_to_database(emoji.id)
            emojis_dict = {}
            for emoji in list_of_emojis:
                field = collection.find({"_id": emoji.id}, {"count": 1})
                for values in field:
                    id = values["_id"]
                    count = values["count"]
                emojis_dict.update({id: count})
            sorted_emotes = OrderedDict(sorted(emojis_dict.items(), key=lambda x: (-x[1], (self.bot.get_emoji(x[0]).name).lower())))
            x = 0
            n = math.ceil(len(list_of_emojis) / 10)
            sorted_emotes_in_tens = [[] for i in range(n)]
            sorted_emotes_values_in_tens = [[] for i in range(n)]
            usage_list = [0 for i in range(n)]
            for key, value in sorted_emotes.items():
                index = math.floor(x/10)
                sorted_emotes_in_tens[index].append(key)
                sorted_emotes_values_in_tens[index].append(value)
                usage_list[index] += value
                x += 1
            total = len(list_of_emojis)   
            for i in range(n):
                try:
                    usage_activity = usage_list[i] / total
                except ZeroDivisionError:
                    usage_activity = 0
                pg_num = i + 1
                fraction = f'{usage_list[i]}/{total}'
                collection.insert_one({"pg_num": pg_num,
                                        "sorted_emotes": sorted_emotes_in_tens[i],
                                        "sorted_emotes_values": sorted_emotes_values_in_tens[i],
                                        "usage_activity": f'{fraction} ({usage_activity: .2f}%)'})
            first_pg_message = collection.find({"pg_num": 1}, {"_id": 0})
            for values in first_pg_message:
                pg_num = values["pg_num"]
                emojis_list = values["sorted_emotes"]
                emojis_value_list = values["sorted_emotes_values"]
                usage_activity = values["usage_activity"]
            embed = discord.Embed(
                title = "Emotes",
                description = f'Total: {total}\n Usage Activity: {usage_activity}',
                colour = discord.Colour.blue(),
            )
            embed.set_footer(text=f'Page: {pg_num}/{n}')
            n = len(emojis_list)
            for i in range(n):
                emoji = self.bot.get_emoji(emojis_list[i])
                count = emojis_value_list[i]
                embed.add_field(name=emoji.name, value=f'{1+i}. {emoji}: {count}', inline=False)
            reaction_message = await ctx.send(embed=embed)
            await reaction_message.add_reaction('◀️')
            await reaction_message.add_reaction('▶️')

            # for key, value in sorted_emotes.items():
            #     await ctx.send(f'{self.bot.get_emoji(key)} {value}')
                # else:
                #     entries = collection.find(query)
                #     for entry in entries:
                #         count = entry["count"]
                #     count += 1
                #     collection.update_one({"_id": emoji.id}, {"$set":{"count": count}})
        # elif collection_size != len(list_of_emojis) and collection_size != 0:
        #     list_of_removed_emojis = []
        #     for id in self.serverEmotes.emojis_dict:
        #         emoji = self.bot.get_emoji(id)
        #         if emoji == None:
        #             list_of_removed_emojis.append(id)
        #     if list_of_removed_emojis:
        #         for id in list_of_removed_emojis:
        #             count = self.serverEmotes.emojis_dict.get(id)
        #             self.serverEmotes.total -= count
        #             del self.serverEmotes.emojis_dict[id]
        #     for emoji in list_of_emojis:
        #         count = self.serverEmotes.emojis_dict.get(emoji.id, -1)
        #         if count == -1:
        #             self.serverEmotes.emojis_dict.update({emoji.id: 0})
        #     self.serverEmotes.embed_list.clear()
        #     n = math.ceil(len(list_of_emojis) / 10)
        #     for x in range(n):
        #         embed = discord.Embed(
        #         title = "Emotes",
        #         description = "",
        #         colour = discord.Colour.blue()
        #         )
        #         pg_num = f'Page {x+1}/{n}'
        #         embed.set_footer(text=pg_num)
        #         self.serverEmotes.embed_list.append(embed)
        #     x = 0
        #     usage_list = []
        #     usage = 0
        #     sorted_emotes = OrderedDict(sorted(self.serverEmotes.emojis_dict.items(), key=lambda x: (-x[1], (self.bot.get_emoji(x[0]).name).lower())))
        #     for id, count in sorted_emotes.items():
        #             index = math.floor(x/10)
        #             emoji = self.bot.get_emoji(id)
        #             usage += count
        #             message = f'{x+1}. {emoji}: {count}'
        #             self.serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
        #             x += 1
        #             if x % 10 == 0:
        #                 usage_list.append(usage)
        #                 usage = 0
        #     n = len(usage_list)
        #     total = self.serverEmotes.total
        #     for x in range(n):
        #         usage = usage_list[x]
        #         try:
        #             usage_activity = (usage / total) * 100
        #         except ZeroDivisionError:
        #             usage_activity = usage
        #         self.serverEmotes.embed_list[x].description = f'Total Count: {total} \n Usage Activity: {usage}/{total} ({usage_activity: .2f}%)'
        #     reactionMessage = await ctx.send(embed=self.serverEmotes.embed_list[0])
        #     await reactionMessage.add_reaction('◀️')
        #     await reactionMessage.add_reaction('▶️')
        # elif collection_size == len(list_of_emojis):
        #     list_of_removed_emojis = []
        #     for id in self.serverEmotes.emojis_dict:
        #         emoji = self.bot.get_emoji(id)
        #         if emoji == None:
        #             list_of_removed_emojis.append(id)
        #     if list_of_removed_emojis:
        #         for id in list_of_removed_emojis:
        #             del self.serverEmotes.emojis_dict[id]
        #     for emoji in list_of_emojis:
        #         count = self.serverEmotes.emojis_dict.get(emoji.id, -1)
        #         if count == -1:
        #             self.serverEmotes.emojis_dict.update({emoji.id: 0})
        #     for embeds in self.serverEmotes.embed_list:
        #         embeds.clear_fields()
        #     x = 0
        #     usage_list = []
        #     usage = 0
        #     sorted_emotes = OrderedDict(sorted(self.serverEmotes.emojis_dict.items(), key=lambda x: (-x[1], (self.bot.get_emoji(x[0]).name).lower())))
        #     for id, count in sorted_emotes.items():
        #         index = math.floor(x/10)
        #         emoji = self.bot.get_emoji(id)
        #         usage += count
        #         message = f'{x+1}. {emoji}: {count}'
        #         self.serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
        #         x += 1
        #         if x % 10 == 0:
        #             usage_list.append(usage)
        #             usage = 0
        #     n = len(usage_list)
        #     total = self.serverEmotes.total
        #     for x in range(n):
        #         usage = usage_list[x]
        #         try:
        #             usage_activity = (usage / total) * 100
        #         except ZeroDivisionError:
        #             usage_activity = usage
        #         self.serverEmotes.embed_list[x].description = f'Total Count: {total} \n Usage Activity: {usage}/{total} ({usage_activity: .2f}%)' 
        #     reactionMessage = await ctx.send(embed=self.serverEmotes.embed_list[0]) 
        #     await reactionMessage.add_reaction('◀️')
        #     await reactionMessage.add_reaction('▶️')
        # else:
        #     n = math.ceil(len(list_of_emojis) / 10)
        #     for x in range(n):
        #         embed = discord.Embed(
        #         title = "Emotes",
        #         description = "",
        #         colour = discord.Colour.blue()
        #         )
        #         pg_num = f'Page {x+1}/{n}'
        #         embed.set_footer(text=pg_num)
        #         self.serverEmotes.embed_list.append(embed)
        #     for emoji in list_of_emojis:
        #         self.serverEmotes.emojis_dict.update({emoji.id: 0})
        #     x = 0
        #     sorted_emotes = OrderedDict(sorted(self.serverEmotes.emojis_dict.items(), key=lambda x: (self.bot.get_emoji(x[0]).name).lower()))
        #     for id, count in sorted_emotes.items():
        #             index = math.floor(x/10)
        #             emoji = self.bot.get_emoji(id)
        #             message = f'{x+1}. {emoji}: {count}'
        #             self.serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
        #             x += 1
        #     n = len(self.serverEmotes.embed_list)
        #     total = self.serverEmotes.total
        #     usage = 0
        #     usage_activity = 0
        #     for x in range(n):
        #         self.serverEmotes.embed_list[x].description = f'Total Count: {total}\n Usage Activity: {usage}/{total} ({usage_activity: .2f}%)'
        #     reactionMessage = await ctx.send(embed=self.serverEmotes.embed_list[0])
        #     await reactionMessage.add_reaction('◀️')
        #     await reactionMessage.add_reaction('▶️')

def setup(bot):
    bot.add_cog(EmoteCommand(bot))