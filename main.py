<<<<<<< HEAD
import os
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

# Load extensions (events and commands)
bot.load_extension('code.events')
bot.load_extension('code.admin_commands')
bot.load_extension('code.user_commands')
bot.load_extension('code.auto_moderator')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

=======
import os
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

# Load extensions (events and commands)
bot.load_extension('code.events')
bot.load_extension('code.admin_commands')
bot.load_extension('code.user_commands')
bot.load_extension('code.auto_moderator')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

>>>>>>> 8267c46fc0b19acd67be4db332cbd2f23e749d22
bot.run(token)