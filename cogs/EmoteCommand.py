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
        collection.remove({"current_pg": 1})
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
                if (collection.count_documents({"emoji_id": emoji.id}) == 0):
                    EmoteCommand.insert_new_emoji_to_database(emoji.name, emoji.id)
            emojis_dict = EmoteCommand.create_emojis_dictionary(list_of_emojis)
            sorted_emotes = OrderedDict(sorted(emojis_dict.items(), key=lambda x: (-x[1], (self.bot.get_emoji(x[0]).name).lower())))
            if (collection.count_documents({"message_type": "embed"}) > 0):
                EmoteCommand.remove_previous_embed_documents()
            if (collection.count_documents({"current_pg": 1}) > 0):
                EmoteCommand.remove_previous_page_document()
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

def setup(bot):
    bot.add_cog(EmoteCommand(bot))