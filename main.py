import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)

async def load_extensions():
    await bot.load_extension('code.events')
    await bot.load_extension('code.admin_commands')
    await bot.load_extension('code.user_commands')
    await bot.load_extension('code.auto_moderator')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

asyncio.run(main())
