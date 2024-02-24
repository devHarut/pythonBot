import discord
from discord.ext import commands, bridge
import random
import math

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @bridge.bridge_group()
    async def random(self, ctx):
        pass

    # Random number generator
    @random.command(description="Generate a random number")
    async def number(self, ctx, lowernumber:int, uppernumber:int):
        number = random.randrange(lowernumber, uppernumber)
        await ctx.respond(f"Your random numbner in range of {lowernumber} and {uppernumber} is number {number}")

    # Get a message's ID
    @discord.message_command()
    async def getmessageid(self, ctx, message:discord.Message):
        await ctx.respond(f"{message.id}", ephemeral=True)

    # Get a user's ID
    @discord.user_command()
    async def getuserid(self, ctx, user:discord.User):
        await ctx.respond(f"{user.id}", ephemeral=True)

    # Generate a random color (Work In Progress)
    @random.command(description="Generate a random color!")
    async def color(self, ctx):
        await ctx.defer()
        rcolor = lambda: random.randint(0, 255)
        color = "#%02X%02X%02X" % (rcolor(), rcolor(), rcolor())
        color = color.replace("#", "")
        crgblink = f"https://some-random-api.ml/canvas/misc/rgb?hex={color}"
        crgbpage = urlopen(crgblink)
        crgbbytes = crgbpage.read()
        crgbdecode = crgbbytes.decode("utf-8")
        crgb0 = crgbdecode.replace("{\"r\":", "")
        crgb1 = crgb0.replace("\"g\":", "")
        crgb2 = crgb1.replace("\"b\":", "")
        crgb3 = crgb2.replace("}", "")
        crgb = crgb3.replace(",", ", ")
        embed = discord.Embed(title=f"#{color}", description=f"Random Color")
        embed.add_field(name=f"RGB", value=f"{crgb}")
        embed.set_image(url=f"https://some-random-api.ml/canvas/misc/colorviewer?hex={color}")
        await ctx.respond(embed=embed)

    # View another user's avatar
    @bridge.bridge_command(description="See another member's avatar")
    async def avatar(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"{str(member)}'s avatar:", color=random.randrange(0, 0xffffff))
        embed.set_image(url=member.avatar.url)
        await ctx.respond(embed=embed)

    # Math Commands (So far we have Addition, Subtraction, Multiplication, Division) (I may add square root and number to the power of)
    @bridge.bridge_group()
    async def math(self, ctx):
        pass

    @math.command(description="Add a number to another number")
    async def add(self, ctx, firstnumber:int, secondnumber:int):
        await ctx.respond(f"{firstnumber}+{secondnumber} = {firstnumber+secondnumber}")

    @math.command(description="Subtract a number from another number")
    async def subtract(self, ctx, firstnumber:int, secondnumber:int):
        await ctx.respond(f"{firstnumber}-{secondnumber} = {firstnumber-secondnumber}")

    @math.command(description="Multiply a number with another number")
    async def multiply(self, ctx, firstnumber:int, secondnumber:int):
        await ctx.respond(f"{firstnumber}x{secondnumber} = {firstnumber*secondnumber}")

    @math.command(description="Divide a number with another number")
    async def divide(self, ctx, firstnumber:int, secondnumber:int):
        await ctx.respond(f"{firstnumber}/{secondnumber} = {firstnumber/secondnumber}")

    @bridge.bridge_command(description="Get information about the server")
    async def serverinfo(self, ctx):
        id = ctx.guild.id
        txt = len(ctx.guild.text_channels)
        vc = len(ctx.guild.voice_channels)
        time = str(ctx.guild.created_at)
        owner = ctx.guild.owner
        embed = discord.Embed(title=f"{ctx.guild.name}")
        embed.add_field(name="Server Members", value=f"{ctx.guild.member_count}")
        embed.add_field(name="Server Owner", value=owner)
        embed.add_field(name="Created at", value=f"{time}")
        embed.add_field(name="Text Channels", value=f"{txt}")
        embed.add_field(name="Voice Channels", value=f"{vc}")
        embed.add_field(name="Server ID", value=f"{id}")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))