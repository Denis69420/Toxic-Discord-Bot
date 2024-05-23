import discord
from discord.ext import commands
import json
import os

config_file_path = 'code/config.json'

def setup(bot: commands.Bot):
    @bot.event
    async def on_ready():
        print(f'Bot is ready and logged in as {bot.user.name} ({bot.user.id})')

    @bot.event
    async def on_guild_join(guild: discord.Guild):
        if not os.path.exists(config_file_path):
            with open(config_file_path, 'w') as f:
                json.dump({}, f)

        with open(config_file_path, 'r') as f:
            config = json.load(f)

        if str(guild.id) not in config:
            config[str(guild.id)] = {}

        with open(config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        print(f'Joined new guild: {guild.name} (ID: {guild.id})')

    @bot.event
    async def on_member_join(member: discord.Member):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(member.guild.id)
        channel_id = config.get(guild_id, {}).get('welcome_channel_id')
        if channel_id:
            channel = bot.get_channel(int(channel_id))
            if channel:
                await channel.send(f'Welcome to the server, {member.mention}!')
            else:
                print(f"Channel with ID {channel_id} not found in guild {guild_id}.")
        else:
            print(f"Welcome channel ID not set for guild {guild_id}.")

    @bot.event
    async def on_member_remove(member: discord.Member):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(member.guild.id)
        channel_id = config.get(guild_id, {}).get('leave_channel_id')
        if channel_id:
            channel = bot.get_channel(int(channel_id))
            if channel:
                await channel.send(f'{member.mention} has left the server.')
            else:
                print(f"Channel with ID {channel_id} not found in guild {guild_id}.")
        else:
            print(f"Leave channel ID not set for guild {guild_id}.")