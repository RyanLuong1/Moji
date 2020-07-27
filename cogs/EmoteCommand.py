from discord.ext import commands
from collections import OrderedDict
from Connection import Connect
from pymongo import MongoClient
import math
import discord
cluster = Connect.get_connect()
db = cluster['emotes']
collection = db['emotes']

#TODO: Emotes are inserted 0-8 instead of 0-9

class EmoteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def reset_database():
        collection.remove({})

    def insert_new_emoji_to_database(emoji_name, emoji_id):
        entry = {"emoji_name": emoji_name ,"emoji_id": emoji_id, "count": 0}
        collection.insert_one(entry)
    """
    (bot.get_emoji(x[0]).name).lower() -> Gets the lowercase version of the emojis names
    (-x[1], (bot.get_emoji(x[0]).name)).lower())) -> Sort the dict by value in descending order then by the lowercase version of the emojis names in ascending order
    Sorting the emojis by count descendingly then by name ascendingly makes the list look ordered
    """

    @commands.command(name="reset")
    async def reset(self, ctx):
        if (ctx.message.author.id == 168194032600743936):
            EmoteCommand.reset_database()
            await ctx.send("Database reset!")
        else:
            await ctx.send("Sorry! Only Ryan has access to it")

    @commands.command(name='emotes')
    async def emotes(self ,ctx):
        list_of_emojis = ctx.guild.emojis
        if not list_of_emojis:
            await ctx.send(f'Your server does not have any custom emotes!')
        else:
            for emoji in list_of_emojis:
                query = {"emoji_id": emoji.id}
                if (collection.count_documents(query) == 0):
                    EmoteCommand.insert_new_emoji_to_database(emoji.name, emoji.id)
            emojis_dict = {}
            for emoji in list_of_emojis:
                document = collection.find({"emoji_id": emoji.id}, {"_id": 0})
                for fields in document:
                    emoji_id = fields["emoji_id"]
                    count = fields["count"]
                emojis_dict.update({emoji_id: count})
            sorted_emotes = OrderedDict(sorted(emojis_dict.items(), key=lambda x: (-x[1], (self.bot.get_emoji(x[0]).name).lower())))
            query = {"message_type": "embed"}
            if (collection.count_documents(query) > 0):
                collection.delete_many(query)
            query = {"current_pg": 1}
            if (collection.count_documents(query) > 0):
                collection.remove(query)
            x = 0
            n = math.ceil(len(list_of_emojis) / 10)
            total_count = 0
            sorted_emotes_in_tens = [[] for i in range(n)]
            sorted_emotes_values_in_tens = [[] for i in range(n)]
            usage_list = [0 for i in range(n)]
            for key, value in sorted_emotes.items():
                index = math.floor(x/10)
                sorted_emotes_in_tens[index].append(key)
                sorted_emotes_values_in_tens[index].append(value)
                usage_list[index] += value
                total_count += value
                x += 1
            for i in range(n):
                try:
                    usage_activity = usage_list[i] / total_count
                except ZeroDivisionError:
                    usage_activity = 0
                pg_num = i + 1
                fraction = f'{usage_list[i]}/{total_count}'
                collection.insert_one({"message_type": "embed",
                                        "pg_num": pg_num,
                                        "sorted_emotes": sorted_emotes_in_tens[i],
                                        "sorted_emotes_values": sorted_emotes_values_in_tens[i],
                                        "usage_activity": f'{fraction} ({usage_activity: .2f}%)',
                                        "total_count": total_count})
            collection.insert_one({"max_pgs": n, "current_pg": 1})
            first_pg_message_document = collection.find({"pg_num": 1}, {"_id": 0})
            for fields in first_pg_message_document:
                pg_num = fields["pg_num"]
                emojis_list = fields["sorted_emotes"]
                emojis_value_list = fields["sorted_emotes_values"]
                usage_activity = fields["usage_activity"]
            embed = discord.Embed(
                title = "Emotes",
                description = f'Total Count: {total_count}\n Usage Activity: {usage_activity}',
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
        #             self.serverEmotes.from emojibotclass import EmojiClassembed_list[index].add_field(name=emoji.name, value=message, inline=False)
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