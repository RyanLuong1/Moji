from discord.ext import commands
from collections import OrderedDict
from emojibotclass import EmojiClass
import math
import discord
class EmoteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.serverEmotes = EmojiClass()

    
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
        elif len(self.serverEmotes.emojis_dict) != len(list_of_emojis) and len(self.serverEmotes.emojis_dict) != 0:
            list_of_removed_emojis = []
            for id in self.serverEmotes.emojis_dict:
                emoji = self.bot.get_emoji(id)
                if emoji == None:
                    list_of_removed_emojis.append(id)
            if list_of_removed_emojis:
                for id in list_of_removed_emojis:
                    count = self.serverEmotes.emojis_dict.get(id)
                    self.serverEmotes.total -= count
                    del self.serverEmotes.emojis_dict[id]
            for emoji in list_of_emojis:
                count = self.serverEmotes.emojis_dict.get(emoji.id, -1)
                if count == -1:
                    self.serverEmotes.emojis_dict.update({emoji.id: 0})
            self.serverEmotes.embed_list.clear()
            n = math.ceil(len(list_of_emojis) / 10)
            for x in range(n):
                embed = discord.Embed(
                title = "Emotes",
                description = "",
                colour = discord.Colour.blue()
                )
                pg_num = f'Page {x+1}/{n}'
                embed.set_footer(text=pg_num)
                self.serverEmotes.embed_list.append(embed)
            x = 0
            usage_list = []
            usage = 0
            sorted_emotes = OrderedDict(sorted(self.serverEmotes.emojis_dict.items(), key=lambda x: (-x[1], (self.bot.get_emoji(x[0]).name).lower())))
            for id, count in sorted_emotes.items():
                    index = math.floor(x/10)
                    emoji = self.bot.get_emoji(id)
                    usage += count
                    message = f'{x+1}. {emoji}: {count}'
                    self.serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
                    x += 1
                    if x % 10 == 0:
                        usage_list.append(usage)
                        usage = 0
            usage = 0
            n = len(usage_list)
            total = self.serverEmotes.total
            for x in range(n):
                usage = usage_list[x]
                usage_activity = (usage / total) * 100
                self.serverEmotes.embed_list[x].description = f'Total Count: {total} \n Usage Activity: {usage}/{total} ({usage_activity: .2f}%)'
            reactionMessage = await ctx.send(embed=self.serverEmotes.embed_list[0])
            await reactionMessage.add_reaction('◀️')
            await reactionMessage.add_reaction('▶️')
        elif len(self.serverEmotes.emojis_dict) == len(list_of_emojis):
            list_of_removed_emojis = []
            for id in self.serverEmotes.emojis_dict:
                emoji = self.bot.get_emoji(id)
                if emoji == None:
                    list_of_removed_emojis.append(id)
            if list_of_removed_emojis:
                for id in list_of_removed_emojis:
                    del self.serverEmotes.emojis_dict[id]
            for emoji in list_of_emojis:
                count = self.serverEmotes.emojis_dict.get(emoji.id, -1)
                if count == -1:
                    self.serverEmotes.emojis_dict.update({emoji.id: 0})
            for embeds in self.serverEmotes.embed_list:
                embeds.clear_fields()
            x = 0
            usage_list = []
            usage = 0
            sorted_emotes = OrderedDict(sorted(self.serverEmotes.emojis_dict.items(), key=lambda x: (-x[1], (self.bot.get_emoji(x[0]).name).lower())))
            for id, count in sorted_emotes.items():
                index = math.floor(x/10)
                emoji = self.bot.get_emoji(id)
                usage += count
                message = f'{x+1}. {emoji}: {count}'
                self.serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
                x += 1
                if x % 10 == 0:
                    usage_list.append(usage)
                    usage = 0
            usage = 0
            n = len(usage_list)
            total = self.serverEmotes.total
            for x in range(n):
                usage = usage_list[x]
                usage_activity = (usage / total) * 100
                self.serverEmotes.embed_list[x].description = f'Total Count: {total} \n Usage Activity: {usage}/{total} ({usage_activity: .2f}%)' 
            reactionMessage = await ctx.send(embed=self.serverEmotes.embed_list[0]) 
            await reactionMessage.add_reaction('◀️')
            await reactionMessage.add_reaction('▶️')
        else:
            n = math.ceil(len(list_of_emojis) / 10)
            for x in range(n):
                embed = discord.Embed(
                title = "Emotes",
                description = "",
                colour = discord.Colour.blue()
                )
                pg_num = f'Page {x+1}/{n}'
                embed.set_footer(text=pg_num)
                self.serverEmotes.embed_list.append(embed)
            for emoji in list_of_emojis:
                self.serverEmotes.emojis_dict.update({emoji.id: 0})
            x = 0
            sorted_emotes = OrderedDict(sorted(self.serverEmotes.emojis_dict.items(), key=lambda x: (self.bot.get_emoji(x[0]).name).lower()))
            for id, count in sorted_emotes.items():
                    index = math.floor(x/10)
                    emoji = self.bot.get_emoji(id)
                    message = f'{x+1}. {emoji}: {count}'
                    self.serverEmotes.embed_list[index].add_field(name=emoji.name, value=message, inline=False)
                    x += 1
            n = len(self.serverEmotes.embed_list)
            total = self.serverEmotes.total
            usage = 0
            usage_activity = 0
            for x in range(n):
                self.serverEmotes.embed_list[x].description = f'Total Count: {total}\n Usage Activity: {usage}/{total} ({usage: .2f}%)'
            reactionMessage = await ctx.send(embed=self.serverEmotes.embed_list[0])
            await reactionMessage.add_reaction('◀️')
            await reactionMessage.add_reaction('▶️')

def setup(bot):
    bot.add_cog(EmoteCommand(bot))