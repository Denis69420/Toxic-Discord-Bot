import discord
from discord.ext import commands
import json

# Define the path to the server configuration file
config_file_path = 'config.json'

# Define a dictionary to store localization data
locales = {}

class LanguageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setlang')
    @commands.has_permissions(administrator=True)
    async def set_language(self, ctx, lang: str):
        """Set the language for the server."""
        if lang not in locales:
            await ctx.send("Unsupported language.")
            return
        
        with open(config_file_path, 'r') as f:
            config = json.load(f)
        
        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {}

        config[guild_id]['language'] = lang

        with open(config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f"Language has been set to {lang}.")

# Load the cog when the bot starts
async def setup(bot: commands.Bot):
    await bot.add_cog(LanguageCommands(bot))
