from discord.ext import commands
from Connection import Connect
from pymongo import MongoClient

import re
import discord

cluster = Connect.get_connect()
db = cluster['emotes']
collection = db['emotes']

class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def insert_new_emoji_to_database(emoji):
        entry = {"emoji_name": emoji.name ,"emoji_id": emoji.id, "count": 0}
        collection.insert_one(entry)
    
    def remove_emoji_from_database(emoji):
        collection.remove({"emoji_id": emoji.id})

    def update_emoji_name_in_database(emoji):
        collection.update_one({"emoji_id": emoji.id}, {"$set":{"emoji_name": emoji.name}})
        
    def get_new_emoji(new_emojis_list):
        return new_emojis_list[-1]
    
    """
    Check the first or the last emoji of the old list to see if it is not in the new list
    before iterating the old list to find the removed emoji
    """
    
    def get_removed_emoji(old_emojis_list, new_emojis_list):
        if old_emojis_list[0] not in new_emojis_list:
            removed_emoji = old_emojis_list[0]
        elif old_emojis_list[-1] not in new_emojis_list:
            removed_emoji = old_emojis_list[-1]
        else:
            for emoji in old_emojis_list:
                if emoji not in new_emojis_list:
                    removed_emoji = emoji
                    break
        return removed_emoji

    """
    Check if the first or the last emoji name is not in the database
    before iterating the new list to find which emoji name is not in it  
    """

    def get_changed_emoji(new_emojis_list):
        if collection.count_documents({"emoji_name": new_emojis_list[0].name}) == 0:
            changed_emoji = new_emojis_list[0]
        elif collection.count_documents({"emoji_name": new_emojis_list[-1].name}) == 0:
            changed_emoji = new_emojis_list[-1]
        else:
            for emoji in new_emojis_list:
                if collection.count_documents({"emoji_name": emoji.name}) == 0:
                    changed_emoji = emoji
                    break
        return changed_emoji

    def increment_emoji_count(emoji):
        field = collection.find({"emoji_id": emoji.id}, {"_id": 0})
        for value in field:
            count = value["count"]
        count += 1
        collection.update_one({"emoji_id": emoji.id}, {"$set":{"count": count}})
    
    def get_current_and_max_pages():
        page_document = collection.find({"current_pg": {'$exists': 'true'}})
        for values in page_document:
            max_pgs = values["max_pgs"]
            current_pg = values["current_pg"]
        return current_pg, max_pgs

    def go_to_next_page(current_pg, max_pgs):
        if current_pg == max_pgs:
            new_pg = 1
        else:
            new_pg = current_pg + 1
        collection.update_one({"max_pgs": max_pgs}, {"$set":{"current_pg": new_pg}})
        return new_pg
    
    def go_back_a_page(current_pg, max_pgs):
        if current_pg == 1:
            new_pg = max_pgs * 1
        else:
            new_pg = current_pg - 1
        collection.update_one({"max_pgs": max_pgs}, {"$set":{"current_pg": new_pg}})
        return new_pg

    def get_new_page_document_values(current_pg):
        next_pg_document = collection.find({"pg_num": current_pg}, {"message_type": 0, "_id": 0})
        for values in next_pg_document:
            sorted_emotes = values["sorted_emotes"]
            sorted_emotes_values = values["sorted_emotes_values"]
            usage_activity = values["usage_activity"]
            total_count = values["total_count"]
        return sorted_emotes, sorted_emotes_values, usage_activity, total_count

    def create_embed_message(total_count, usage_activity, new_pg, max_pgs):
        embed = discord.Embed(
            title = "Emotes",
            description = f'Total Count: {total_count:,}\n Usage Activity: {usage_activity}',
            colour = discord.Colour.blue()
        )
        embed.set_footer(text=f'Page: {new_pg}/{max_pgs}')
        return embed  
    
    def update_embed_with_emoji_info(bot, embed, sorted_emotes, sorted_emotes_values, new_pg):
        n = len(sorted_emotes)
        for i in range(n):
            emoji = bot.get_emoji(sorted_emotes[i])
            count = sorted_emotes_values[i]
            position = ((new_pg - 1) * 10) + (i + 1)
            embed.add_field(name=emoji.name, value=f'{position}, {emoji}: {count:,}', inline=False)
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        emojis_list = guild.emojis
        for emoji in emojis_list:
            if (collection.count_documents({"emoji_id": emoji.id}) == 0):
                CommandEvents.insert_new_emoji_to_database(emoji.name, emoji.id)
        await self.bot.change_presence(activity = discord.Game(name="Mass Effect"))

    """
    Check 3 conditions: if the new list length is greater, then an emoji was added,
                        if the old list length is greater, then an emoji was removed,
                        or if both list lengths are the same, then an emoji name was changed.
    """

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, old_emojis_list, new_emojis_list):
        old_list_size = len(old_emojis_list)
        new_list_size = len(new_emojis_list)
        if new_list_size > old_list_size:
            new_emoji = CommandEvents.get_new_emoji(new_emojis_list)
            CommandEvents.insert_new_emoji_to_database(new_emoji)
        elif old_list_size > new_list_size:
            removed_emoji = CommandEvents.get_removed_emoji(old_emojis_list, new_emojis_list)
            CommandEvents.remove_emoji_from_database(removed_emoji)
        else:
            changed_emoji = CommandEvents.get_changed_emoji(new_emojis_list)
            CommandEvents.update_emoji_name_in_database(changed_emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        bot = self.bot
        reaction_message = reaction.message
        if user.bot:
            return
        elif not reaction_message.embeds:
            if collection.count_documents({"emoji_id": reaction.emoji.id}) != 0:
                CommandEvents.increment_emoji_count(reaction.emoji)
        else:
            if reaction_message.embeds[0].title == "Emotes":
                current_pg, max_pgs = CommandEvents.get_current_and_max_pages()
                if reaction.emoji == '◀️':
                    new_pg = CommandEvents.go_back_a_page(current_pg, max_pgs)
                elif reaction.emoji == '▶️':
                    new_pg = CommandEvents.go_to_next_page(current_pg, max_pgs)
                sorted_emotes, sorted_emotes_values, usage_activity, total_count = CommandEvents.get_new_page_document_values(new_pg)
                embed = CommandEvents.create_embed_message(total_count, usage_activity, new_pg, max_pgs)
                updated_embed = CommandEvents.update_embed_with_emoji_info(bot, embed, sorted_emotes, sorted_emotes_values, new_pg)
                await reaction.remove(user)
                await reaction_message.edit(embed=updated_embed)
            else:
                if collection.count_documents({"emoji_id": reaction.emoji.id}) != 0:
                    CommandEvents.increment_emoji_count(reaction.emoji)

    """
    Discord bots write emotes as <:name_of_emotes:#>.
    Parsing the message to get the emojis ids is better since ids are unique, but names are not 
    Find the emojis ids by using the following pattern, a group of numbers that ends with a >.
    """
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        list_of_emojis_ids = re.findall(r"(\d+.)\>", str(message.content))
        for emoji_id in list_of_emojis_ids:
            if collection.count_documents({"emoji_id": int(emoji_id)}) != 0:
                emoji = self.bot.get_emoji(int(emoji_id))
                CommandEvents.increment_emoji_count(emoji)

    
def setup(bot):
    bot.add_cog(CommandEvents(bot))
