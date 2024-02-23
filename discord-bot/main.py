import discord
import asyncio
import random
import time
import aiohttp
import os
from discord.ext.pages import Paginator, Page
from discord.ext import bridge, commands
from dotenv import load_dotenv

load_dotenv()

class CustomHelpCommand(commands.DefaultHelpCommand):
    pass

class pythonBot(bridge.Bot):
    TOKEN = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.all()
    help_command = CustomHelpCommand()

client = pythonBot(intents=pythonBot.intents, command_prefix="_", help_command=pythonBot.help_command)

# Error Handling
@client.event
async def on_application_command_error(ctx:discord.ApplicationContext, error:discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown!", ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond("You do not have the required permissions to run this command!", ephemeral=True)
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.respond("I do not have enough permissions to do this!")
    elif isinstance(error, commands.NSFWChannelRequired):
        await ctx.respond("This command can only be used in an NSFW Channel!", ephemeral=True)
    else:
        raise error

@client.listen()
async def on_ready():
    print(f"Logged in as {client.user.name}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))

@client.bridge_command(description = "Ping, pong!")
async def ping(ctx):
    latency = (str(client.latency)).split(".")[1][1:3]
    await ctx.respond(f"Pong! Bot replied in {latency} ms")

pages = [
    Page(
        embeds=[
            discord.Embed(title="pythonBot", description="pythonBot is a multipurpose bot offering moderation, utility commands, autromod, fun commands, ticketing system, AFK system and economy")
        ],
    ),
    Page(
        embeds=[
            discord.Embed(title="Moderation", description="**/ban (member)\n/kick (member)\n/timeout (member) (days) (hours) (minutes)\n/purge (member is optional) (amount of messages)**")
        ],
    ),
    Page(
        embeds=[
            discord.Embed(title="Utilities", description="**/random number (min number) (max number)\n/random color is W.I.P\n/avatar (member)**")
        ],
    ),
]

@client.bridge_command(description="Information about the bot")
async def help(ctx):
    paginator = Paginator(pages=pages)
    try:
        await paginator.respond(ctx.interaction)
    except:
        await paginator.send(ctx)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded {filename}")

async def main_bot():
    print("Bot is starting...")
    await client.start(pythonBot().TOKEN)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main_bot()))
