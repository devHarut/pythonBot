import discord
from discord.ext import commands, bridge
import asyncio

class ServerLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Logs Deleted Messages
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        for channel in message.author.guild.channels:
            if str(channel.name) == "server-logs":
                msg_del = str(f"{message.content}")
                auth_name = str(f"{message.author}")
                ch_name = str(f"{message.channel.name}")
                embed = discord.Embed(color=discord.Colour.dark_orange())
                embed.set_author(name="Message deleted")
                embed.add_field(name=f"Message", value=msg_del, inline=False)
                embed.add_field(name=f"Message author", value=auth_name, inline=False)
                embed.add_field(name=f"Channel", value=ch_name, inline=False)
                await channel.send(embed=embed)

    # Logs Edited Messages
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        blue = discord.Colour.blue()
        guild = before.author.guild
        embed = discord.Embed(title=f"{before.author} edited a message", color=blue)
        embed.add_field(name=before.content, value="This is the message before the edit", inline=True)
        embed.add_field(name=after.content, value="This is the message after the edit", inline=True)
        for channel in guild.channels:
            if str(channel.name) == "server-logs":
                await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(ServerLogs(bot))

# https://www.youtube.com/watch?v=m0nAYsIt32o&list=UULF2sojt6JHzoApSkKBvtlurg&index=12