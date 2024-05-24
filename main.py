import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from code.localization import Localization

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='?', intents=intents)
locales = Localization.load_locales('code/locales')

# Load extensions
async def load_extensions():
    await bot.load_extension('code.events')
    await bot.load_extension('code.admin_commands')
    await bot.load_extension('code.user_commands')
    await bot.load_extension('code.auto_moderator')
    await bot.load_extension('code.language_commands')
    await bot.load_extension('code.ticket_system')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

asyncio.run(main())
