import discord
from discord.ext import commands
import json
import os

config_file_path = 'code/config.json'

def setup(bot: commands.Bot):
    @bot.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(ctx: commands.Context, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked.')

    @bot.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(ctx: commands.Context, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned.')

    @bot.command(name='setwelcome')
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(ctx: commands.Context, channel: discord.TextChannel):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {}
        config[guild_id]['welcome_channel_id'] = str(channel.id)

        with open(config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f'Welcome channel has been set to {channel.mention}')

    @bot.command(name='setleave')
    @commands.has_permissions(administrator=True)
    async def set_leave_channel(ctx: commands.Context, channel: discord.TextChannel):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {}
        config[guild_id]['leave_channel_id'] = str(channel.id)

        with open(config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f'Leave channel has been set to {channel.mention}')

    @bot.command(name='addprohibited')
    @commands.has_permissions(administrator=True)
    async def add_prohibited_word(ctx: commands.Context, word: str):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {}

        if 'prohibited_words' not in config[guild_id]:
            config[guild_id]['prohibited_words'] = []

        if word not in config[guild_id]['prohibited_words']:
            config[guild_id]['prohibited_words'].append(word)

        with open(config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f'Added `{word}` to the list of prohibited words.')

    @bot.command(name='removeprohibited')
    @commands.has_permissions(administrator=True)
    async def remove_prohibited_word(ctx: commands.Context, word: str):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {}

        if 'prohibited_words' in config[guild_id] and word in config[guild_id]['prohibited_words']:
            config[guild_id]['prohibited_words'].remove(word)

            with open(config_file_path, 'w') as f:
                json.dump(config, f, indent=4)

            await ctx.send(f'Removed `{word}` from the list of prohibited words.')
        else:
            await ctx.send(f'`{word}` is not in the list of prohibited words.')