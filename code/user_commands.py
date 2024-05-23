import discord
from discord.ext import commands

def setup(bot: commands.Bot):
    @bot.command(name='ping')
    async def ping(ctx: commands.Context):
        await ctx.send('Pong!')