from discord.ext import commands
from Connection import Connect
from pymongo import MongoClient
import re


#TODO: count documents is returning 0 for some reason despite the entry existing in the database

cluster = Connect.get_connect()
db = cluster['emotes']
collection = db['emotes']

class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.author == self.bot.user:
            return
        if not reaction.message.embeds:
            id = reaction.emoji.id
            query = {"emoji_id": int(id)}
            if (collection.count_documents(query) != 0):
                field = collection.find(query, {"_id": 0})
                for value in field:
                    count = value["count"]
                count += 1
                collection.update_one({"emoji_id": int(id)}, {"$set":{"count": count}})
        #     count = self.serverEmotes.emojis_dict.get(id, -1)
        #     if count != -1:
        #         (self.serverEmotes.emojis_dict[id]) += 1
        #         self.serverEmotes.total += 1
        # else:
        #     if reaction.message.embeds[0].title == "Emotes":
        #         if reaction.emoji == '◀️':
        #             if self.serverEmotes.pg_num == 0:
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
        list_of_ids = re.findall(r"(\d+.)\>", str(message.content))
        for id in list_of_ids:
            query = {"emoji_id": int(id)}
            if (collection.count_documents(query) != 0):
                field = collection.find(query, {"_id": 0})
                for value in field:
                    count = value["count"]
                count += 1
                collection.update_one({"emoji_id": int(id)}, {"$set":{"count": count}})

    
def setup(bot):
    bot.add_cog(CommandEvents(bot))
