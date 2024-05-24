import discord
from discord.ext import commands
import json
import os

config_file_path = 'code/config.json'

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot is ready and logged in as {self.bot.user.name} ({self.bot.user.id})')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
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

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return  # Skip bots, including this bot itself

        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(member.guild.id)
        roles = config.get(guild_id, {}).get('roles', {})
        verified_role_id = roles.get('verified')


        channel_id = config.get(guild_id, {}).get('welcome_channel_id')
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                welcome_message = await channel.send(f'Welcome to the server, {member.mention}! Please verify yourself by reacting with ✅.')
                await welcome_message.add_reaction('✅')
            else:
                print(f"Channel with ID {channel_id} not found in guild {guild_id}.")
        else:
            print(f"Welcome channel ID not set for guild {guild_id}.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name != '✅':
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return

        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(guild.id)
        roles = config.get(guild_id, {}).get('roles', {})
        verified_role_id = roles.get('verified')

        if verified_role_id:
            verified_role = guild.get_role(int(verified_role_id))
            if verified_role and verified_role not in member.roles:
                await member.add_roles(verified_role)
                await member.send('You have been verified!')

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(member.guild.id)
        channel_id = config.get(guild_id, {}).get('leave_channel_id')
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                await channel.send(f'{member.mention} has left the server.')
            else:
                print(f"Channel with ID {channel_id} not found in guild {guild_id}.")
        else:
            print(f"Leave channel ID not set for guild {guild_id}.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
