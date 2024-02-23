import discord
from discord.ext import bridge, commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kick Command
    @bridge.bridge_command(description ="Kick a member")
    @bridge.has_permissions(kick_members=True)
    async def kick(Self, ctx, member:discord.Member, reason:str="No reason provided"):
        await ctx.defer()
        if member.guild_permissions.administrator:
            if member.bot:
                pass
            else:
                return await ctx.respond(embed=discord.Embed(title="Failure", description="You can't kick another admin", color=discord.Colour.red()))
            try:
                try:
                    kickembed = discord.Embed(title="Kick", description=f"You have been kicked from{ctx.guild.name}", color=discord.Colour.red())
                    await member.send(embed=kickembed)
                except:
                    pass
                await member.kick(reason=reason)
                embed = discord.Embed(title="Success", description=f"Successfully kicked '{member.name}'", color=discord.Colour.green())
                await ctx.respond(embed=embed)
            except:
                embed = discord.Embed(title="Failure", description=f"Failed to kick '{member.name}'", color=discord.Colour.red())
                await ctx.respond(embed=embed)

    # Ban Command
    @bridge.bridge_command(description = "Ban a member")
    @bridge.has_permissions(ban_members = True)
    async def ban(Self, ctx, member:discord.Member, reason:str="No reason provided"):
        await ctx.defer()
        if member.guild_permissions.administrator:
            if member.bot:
                pass
            else:
                return await ctx.respond(embed=discord.Embed(title="Failure", description="You can't ban another admin", color=discord.Colour.red()))
            try:
                try:
                    banembed = discord.Embed(title="Kick", description=f"You have been kicked from{ctx.guild.name}", color=discord.Colour.red())
                    await member.send(embed=banembed)
                except:
                    pass
                await member.ban(reason=reason)
                embed = discord.Embed(title="Success", description=f"Successfully banned '{member.name}'", color=discord.Colour.green())
                await ctx.respond(embed=embed)
            except:
                embed = discord.Embed(title="Failure", description=f"Failed to ban '{member.name}'", color=discord.Colour.red())
                await ctx.respond(embed=embed)

    # Timeout Command
    @bridge.bridge_command(description="Timeout another member")
    @bridge.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member:discord.Member, days:int=0, hours:int=0, minutes:int=0):
        duration = timedelta(minutes=minutes, hours=hours, days=days)
        if days == 0 and hours == 0 and minutes == 0:
            return await ctx.respond("Duration can't be 0 days, 0 hours, and 0 minutes!", ephemeral=True)
        await member.timeout_for(duration)
        embed = discord.Embed(title="Success!", description=f"Successfully timed out '{member.mention}' for {days} days, {hours} hours, and {minutes} minutes", color=discord.Colour.green())
        await ctx.respond(embed=embed, ephemeral=True)
        embed2 = discord.Embed(title="Timed out", description=f"You have been timed out for {days} days, {hours} hours and {minutes} minutes in {ctx.guild.name}", color=discord.Colour.red())
        try:
            await member.send(embed=embed)
        except:
            pass

    # Purge Command
    @bridge.bridge_command(description="Delete Messages")
    @bridge.has_permissions(manage_messages=True)
    async def purge(Self, ctx, amount:int, member:discord.Member=None):
        if member !=None:
            msg = []
            async for m in ctx.channel.history():
                if len(msg) == amount:
                    break
                if m.author.id == member.id:
                    msg.append(m)
                await ctx.channel.delete_messages(msg)
                return await ctx.respond(f"Messages from {member.mention} has been purged", ephemeral=True)
        await ctx.respond("Purging messages...", ephemeral=True)
        await ctx.channel.purge(limit=amount)

def setup(bot):
    bot.add_cog(Moderation(bot))