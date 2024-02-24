import discord
from discord.ext import commands, bridge
from datetime import timedelta

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @bridge.bridge_group()
    async def automod():
        pass

    @automod.command(description="Set up the automod system")
    @bridge.has_permissions(administrator=True)
    async def enable(self, ctx):
        await ctx.defer()
        try:
            metadata = discord.AutoModActionMetadata("This message was blocked")
            await ctx.guild.create_auto_moderation_rule(name="Anti-spam", reason="Automod by pythonBot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.spam, trigger_metadata=discord.AutoModTriggerMetadata(), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.guild.create_auto_moderation_rule(name="Block words", reason="Automod by pythonBot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword_preset, trigger_metadata=discord.AutoModTriggerMetadata(presets=[discord.AutoModKeywordPresetType.profanity, discord.AutoModKeywordPresetType.sexual_content, discord.AutoModKeywordPresetType.slurs]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.guild.create_auto_moderation_rule(name="Anti-mention", reason="Automod by pythonBot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.mention_spam, trigger_metadata=discord.AutoModTriggerMetadata(mention_total_limit=5), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.respond("Automod enabled successfully!", ephemeral=True)
        except:
            try:
                rulelist = await ctx.guild.fetch_auto_moderation_rules()
                for rule in rulelist:
                    await rule.delete()
                metadata = discord.AutoModActionMetadata("This message was blocked")
                await ctx.guild.create_auto_moderation_rule(name="Anti-spam", reason="Automod by pythonBot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.spam, trigger_metadata=discord.AutoModTriggerMetadata(), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
                await ctx.guild.create_auto_moderation_rule(name="Block words", reason="Automod by pythonBot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword_preset, trigger_metadata=discord.AutoModTriggerMetadata(presets=[discord.AutoModKeywordPresetType.profanity, discord.AutoModKeywordPresetType.sexual_content, discord.AutoModKeywordPresetType.slurs]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
                await ctx.guild.create_auto_moderation_rule(name="Anti-mention", reason="Automod by pythonBot", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.mention_spam, trigger_metadata=discord.AutoModTriggerMetadata(mention_total_limit=5), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
                await ctx.respond("Automod enabled successfully!", ephemeral=True)
            except:
                await ctx.respond("Failed to enable automod", ephemeral=True)

def setup(bot):
    bot.add_cog(Automod(bot))