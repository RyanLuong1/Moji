from discord.ext import commands
from Connection import Connect
from pymongo import MongoClient
import re
import discord


#TODO: count documents is returning 0 for some reason despite the entry existing in the database

cluster = Connect.get_connect()
db = cluster['emotes']
collection = db['emotes']

class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_pg = 0
        self.max_pgs = 0

    def increment_emoji_count(emoji_id):
        field = collection.find({"emoji_id": emoji_id}, {"_id": 0})
        for value in field:
            count = value["count"]
        count += 1
        collection.update_one({"emoji_id": emoji_id}, {"$set":{"count": count}})
    
    def get_current_and_max_pages():
        page_document = collection.find({"current_pg": {'$exists': 'true'}})
        for values in page_document:
            self.max_pgs = values["max_pgs"]
            self.current_pg = values["current_pg"]

    def go_to_next_page(current_pg, max_pgs):
        if current_pg == max_pgs:
            current_pg = 1
        else:
            current_pg += 1
        collection.update_one({"max_pgs": max_pgs}, {"$set":{"current_pg": current_pg}})
        new_pg = current_pg
        return new_pg
    
    def go_back_a_page(current_pg, max_pgs):
        if current_pg == 1:
            current_pg = max_pgs
        else:
            current_pg -= 1
        collection.update_one({"max_pgs": max_pgs}, {"$set":{"current_pg": current_pg}})
        new_pg = current_pg
        return new_pg

    def get_new_page_document_values(current_pg):
        next_pg_document = collection.find({"pg_num": current_pg}, {"message_type": 0, "_id": 0})
        for values in next_pg_document:
            sorted_emotes = values["sorted_emotes"]
            sorted_emotes_values = values["sorted_emotes_values"]
            usage_activity = values["usage_activity"]
            total_count = values["total_count"]
        return sorted_emotes, sorted_emotes_values, usage_activity, total_count

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "Ryan breaking the bot 24/7"))
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        bot = self.bot
        reaction_message = reaction.message
        if user.bot:
            return
        elif not reaction_message.embeds:
            if (collection.count_documents({"emoji_id": reaction.emoji.id}) != 0):
                CommandEvents.increment_emoji_count(reaction.emoji.id)
        #     count = self.serverEmotes.emojis_dict.get(id, -1)
        #     if count != -1:
        #         (self.serverEmotes.emojis_dict[id]) += 1
        #         self.serverEmotes.total += 1
        else:
            if reaction_message.embeds[0].title == "Emotes":
                current_pg, max_pgs = CommandEvents.get_current_and_max_pages()
                if reaction.emoji == '◀️':
                    new_pg = CommandEvents.go_back_a_page(current_pg, max_pgs)
                elif reaction.emoji == '▶️':
                    new_pg = CommandEvents.go_to_next_page(current_pg, max_pgs)
                await reaction.remove(user)
                sorted_emotes, sorted_emotes_values, usage_activity, total_count = CommandEvents.get_new_page_document_values(new_pg)
                embed = discord.Embed(
                    title = "Emotes",
                    description = f'Total Count: {total_count}\n Usage Activity: {usage_activity}',
                    colour = discord.Colour.blue(),
                )
                embed.set_footer(text=f'Page: {new_pg}/{max_pgs}')
                n = len(sorted_emotes)
                for i in range(n):
                    emoji = self.bot.get_emoji(sorted_emotes[i])
                    count = sorted_emotes_values[i]
                    position = ((current_pg - 1) * 10) + (i + 1)
                    embed.add_field(name=emoji.name, value=f'{position}, {emoji}: {count}', inline=False)
                await reaction_message.edit(embed=embed)
            else:
                if (collection.count_documents({"emoji_id": reaction.emoji.id}) != 0):
                    CommandEvents.increment_emoji_count(reaction.emoji.id)
        #                 self.serverEmotes.pg_num = len(self.serverEmotes.embed_list) - 1
        #                 pg_num = self.serverEmotes.pg_num
        #                 embed = self.serverEmotes.embed_list[pg_num]
        #                 await reaction.message.edit(embed=embed)
        #             else:
        #                 self.serverEmotes.pg_num -= 1
        #                 pg_num = self.serverEmotes.pg_num
        #                 embed = self.serverEmotes.embed_list[pg_num]
        #                 await reaction.message.edit(embed=embed)
        #             await reaction.remove(user)
        #         elif reaction.emoji == '▶️':
        #             if self.serverEmotes.pg_num == len(self.serverEmotes.embed_list) - 1:
        #                 self.serverEmotes.pg_num = 0
        #                 pg_num = self.serverEmotes.pg_num
        #                 embed = self.serverEmotes.embed_list[pg_num]
        #                 await reaction.message.edit(embed=embed)
        #             else:
        #                 self.serverEmotes.pg_num += 1
        #                 pg_num = self.serverEmotes.pg_num
        #                 embed = self.serverEmotes.embed_list[pg_num]
        #                 await reaction.message.edit(embed=embed)
        #             await reaction.remove(user)
        #         else:
        #             id = reaction.emoji.id
        #             count = self.serverEmotes.emojis_dict.get(id, -1)
        #             if count != -1:
        #                 (self.serverEmotes.emojis_dict[id]) += 1
        #                 self.serverEmotes.total += 1

    """
    Discord bots write emotes as <:name_of_emotes:#>.
    Parsing the message to get the emojis ids is a preferable way. 
    Find the emojis ids by using the following pattern, a group of numbers that ends with a >.
    """
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        list_of_emojis_ids = re.findall(r"(\d+.)\>", str(message.content))
        for emoji_id in list_of_emojis_ids:
            if (collection.count_documents({"emoji_id": int(emoji_id)}) != 0):
                CommandEvents.increment_emoji_count(int(emoji_id))

    
def setup(bot):
    bot.add_cog(CommandEvents(bot))
