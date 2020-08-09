from discord.ext import commands
from collections import OrderedDict
from Connection import Connect
from pymongo import MongoClient
from timeit import default_timer as timer

import math
import discord

cluster = Connect.get_connect()
db = cluster['emotes_db']
collection = db['emotes_collection']


class EmoteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def create_emojis_dictionary(list_of_emojis):
        emojis_dict = {}
        for emoji in list_of_emojis:
            document = collection.find({"emoji_id": emoji.id}, {"_id": 0})
            for fields in document:
                emoji_id = fields["emoji_id"]
                count = fields["count"]
            emojis_dict.update({emoji_id: count})
        return emojis_dict
    
    def remove_previous_embed_documents():
        collection.delete_many({"message_type": "embed"}) 

    def remove_previous_page_document():
        collection.remove({"page": "page"})

    def get_sorted_emotes_and_its_values_to_list(sorted_emotes, list_size):
        x = 0
        sorted_emotes_in_tens = [[] for i in range(list_size)]
        sorted_emotes_values_in_tens = [[] for i in range(list_size)]
        for key, value in sorted_emotes.items():
            index = math.floor(x/10)
            sorted_emotes_in_tens[index].append(key)
            sorted_emotes_values_in_tens[index].append(value)
            x += 1  
        return sorted_emotes_in_tens, sorted_emotes_values_in_tens
    
    def get_usage_and_total_count_to_list(sorted_emotes, list_size):
        x = 0
        total_count = 0
        usage_list = [0 for i in range(list_size)]
        for key, value in sorted_emotes.items():
            index = math.floor(x/10)
            usage_list[index] += value
            total_count += value
            x += 1  
        return usage_list, total_count

    def create_embed_documents(sorted_emotes_in_tens, sorted_emotes_values_in_tens, usage_list, total_count, list_size):
        for i in range(list_size):
            try:
                usage_activity = (usage_list[i] / total_count) * 100
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

    def insert_new_page_document(list_size):
        collection.insert_one({"page": "page" ,"max_pgs": list_size, "current_pg": 1})
    
    def get_first_page_values(sorted_emotes_in_tens, sorted_emotes_values_in_tens, usage_list, total_count):
        pg_num = 1
        emojis_list = sorted_emotes_in_tens[0]
        emojis_values_list = sorted_emotes_values_in_tens[0]
        fraction = f'{usage_list[0]}/{total_count}'
        try:
            usage_activity = (usage_list[0] / total_count) * 100
        except ZeroDivisionError:
            usage_activity = 0
        usage_activity = f'{fraction} ({usage_activity: .2f}%)'
        return pg_num, emojis_list, emojis_values_list, usage_activity
    
    def create_embed_message(total_count, usage_activity, pg_num, list_size):
        embed = discord.Embed(
            title = "Emotes",
            description = f'Total Count: {total_count:,}\n Usage Activity: {usage_activity}',
            colour = discord.Colour.blue(),
        )
        embed.set_footer(text=f'Page: {pg_num}/{list_size}')
        return embed

    def update_embed_message_with_emojis_info(bot, embed, emojis_list, emojis_values_list):
        for i in range(10):
            emoji = bot.get_emoji(emojis_list[i])
            count = emojis_values_list[i]
            embed.add_field(name=emoji.name, value=f'{1+i}. {emoji}: {count:,}', inline=False)
        return embed

    """
    (bot.get_emoji(x[0]).name).lower() -> Gets the lowercase version of the emojis names
    (-x[1], (bot.get_emoji(x[0]).name)).lower())) -> Sort the dict by value in descending order then by the lowercase version of the emojis names in ascending order
    """

    @commands.command(name='emotes')
    async def emotes(self ,ctx):
        list_of_emojis = ctx.guild.emojis
        if not list_of_emojis:
            await ctx.send(f'Your server does not have any custom emotes!')
        else:
            emojis_dict = EmoteCommand.create_emojis_dictionary(list_of_emojis)
            sorted_emotes = OrderedDict(sorted(emojis_dict.items(), key=lambda x: (-x[1], (self.bot.get_emoji(x[0]).name).lower())))
            if (collection.count_documents({"message_type": "embed"}) > 0):
                EmoteCommand.remove_previous_embed_documents()
            if (collection.count_documents({"page": "page"}) > 0):
                EmoteCommand.remove_previous_page_document()
            list_size = math.ceil(len(list_of_emojis) / 10)
            sorted_emotes_in_tens, sorted_emotes_values_in_tens = EmoteCommand.get_sorted_emotes_and_its_values_to_list(sorted_emotes, list_size)
            usage_list, total_count = EmoteCommand.get_usage_and_total_count_to_list(sorted_emotes, list_size)
            EmoteCommand.create_embed_documents(sorted_emotes_in_tens, sorted_emotes_values_in_tens, usage_list, total_count, list_size)
            EmoteCommand.insert_new_page_document(list_size)
            pg_num, emojis_list, emojis_values_list, usage_activity = EmoteCommand.get_first_page_values(sorted_emotes_in_tens, sorted_emotes_values_in_tens, usage_list, total_count)
            embed = EmoteCommand.create_embed_message(total_count, usage_activity, pg_num, list_size)
            updated_embed = EmoteCommand.update_embed_message_with_emojis_info(self.bot, embed, emojis_list, emojis_values_list)
            reaction_message = await ctx.send(embed=updated_embed)
            await reaction_message.add_reaction('◀️')
            await reaction_message.add_reaction('▶️')

def setup(bot):
    bot.add_cog(EmoteCommand(bot))
