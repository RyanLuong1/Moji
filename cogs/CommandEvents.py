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

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "Ryan breaking the bot 24/7"))
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        bot = self.bot
        reaction_message = reaction.message
        if user.bot:
            print(f'Reaction made by bot')
            return
        elif not reaction_message.embeds:
            print(f'This is not an embed message')
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
        else:
            print(f'this is a embed message')
            if reaction_message.embeds[0].title == "Emotes":
                field = collection.find({"current_pg": {'$exists': 'true'}})
                for values in field:
                    max_pgs = values["max_pgs"]
                    current_pg = values["current_pg"]
                if reaction.emoji == '◀️':
                    if current_pg == 1:
                        current_pg = max_pgs
                    else:
                        current_pg -= 1
                elif reaction.emoji == '▶️':
                    if current_pg == max_pgs:
                        current_pg = 1
                    else:
                        current_pg += 1
                collection.update_one({"max_pgs": max_pgs}, {"$set":{"current_pg": current_pg}})
                await reaction.remove(user)
                next_pg_document = collection.find({"pg_num": current_pg}, {"message_type": 0, "_id": 0})
                for values in next_pg_document:
                    sorted_emotes = values["sorted_emotes"]
                    sorted_emotes_values = values["sorted_emotes_values"]
                    usage_activity = values["usage_activity"]
                    total_count = values["total_count"]
                embed = discord.Embed(
                    title = "Emotes",
                    description = f'Total Count: {total_count}\n Usage Activity: {usage_activity}',
                    colour = discord.Colour.blue(),
                )
                embed.set_footer(text=f'Page: {current_pg}/{max_pgs}')
                n = len(sorted_emotes)
                for i in range(n):
                    emoji = self.bot.get_emoji(sorted_emotes[i])
                    count = sorted_emotes_values[i]
                    position = ((current_pg - 1) * 10) + (i + 1)
                    embed.add_field(name=emoji.name, value=f'{position}, {emoji}: {count}', inline=False)
                await reaction_message.edit(embed=embed)
            else:
                id = reaction.emoji.id
                query = {"emoji_id": int(id)}
                if (collection.count_documents(query) != 0):
                    field = collection.find(query, {"_id": 0})
                    for value in field:
                        count = value["count"]
                    count += 1
                    collection.update_one({"emoji_id": int(id)}, {"$set":{"count": count}})
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
