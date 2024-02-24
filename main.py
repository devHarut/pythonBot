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

client.persistent_views_added = False

# Ticketing System
class Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        custom_id="ticketing-1",
        placeholder = "Open a ticket",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Report",
                description="Report a user"
            ),
            discord.SelectOption(
                label="Suggestion",
                description="Suggest an improvement for the server"
            ),
            discord.SelectOption(
                label="Other",
                description="Open a ticket for an issue not listed above"
            )
        ]
    )
    async def ticket_callback(self, select, interaction):
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, embed_links=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        }
        channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}', overwrites=overwrites, reason=f"Ticket for {interaction.user.name}")
        await interaction.response.send_message(f"Ticket opened at {channel.mention}", ephemeral=True)
        if select.values[0]=="Report":
            embed = discord.Embed(title="Report a user", description=f"Welcome to your ticket {interaction.user.name}. The support team will be with your shortly. Please specify which user you would like to report and along with the proof.", color=discord.Colour.green())
            await channel.send(embed=embed, view=CloseTicket())
        elif select.values[0]=="Suggestion":
            embed = discord.Embed(title="Suggest an improvement for the server", description=f"Welcome to your ticket {interaction.user.name}. The support team will be with your shortly. Please specify what you would like to suggest.", color=discord.Colour.green())
            await channel.send(embed=embed, view=CloseTicket())
        elif select.values[0]=="Other":
            embed = discord.Embed(title="Open a ticket for an issue not listed above", description=f"Welcome to your ticket {interaction.user.name}. The support team will be with your shortly. Please specify what you need help with.", color=discord.Colour.green())
            await channel.send(embed=embed, view=CloseTicket())

# Close Ticket System
class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close ticket", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="closeticket")
    async def callback(self, button, interaction):
        await interaction.response.send_message("Closing this ticket...")
        await asyncio.sleep(2)
        await interaction.channel.delete()

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
    if not client.persistent_views_added:
        client.add_view(Ticket())
        client.add_view(CloseTicket())
        client.persistent_views_added=True

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
            discord.Embed(title="Moderation", description="**/ban (member) (reason is optional)\n/unban (member_id)\n/kick (member) (reason is optional)\n/timeout (member) (days) (hours) (minutes)\n/purge (amount of messages) (member is optional) **")
        ],
    ),
    Page(
        embeds=[
            discord.Embed(title="Utilities", description="**/ticketing (select the type of ticket in drop down menu)\n/random number (min number) (max number)\n/random color is W.I.P\n/avatar (member)**")
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

@client.bridge_command(description="Start the ticketing system")
@bridge.has_permissions(administrator=True)
async def ticketing(ctx):
    embed = discord.Embed(title="Create a ticket", description="Choose a category below for your ticket", color=discord.Colour.green())
    await ctx.respond("Successfully started ticketing systyem", ephemeral=True)
    await ctx.send(embed=embed, view=Ticket())

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
