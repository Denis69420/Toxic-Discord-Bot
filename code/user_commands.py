import discord
from discord.ext import commands

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context):
        await ctx.send('Pong!')

async def setup(bot: commands.Bot):
    await bot.add_cog(UserCommands(bot))
