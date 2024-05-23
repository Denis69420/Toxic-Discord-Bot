import discord
from discord.ext import commands
import json
import os

config_file_path = 'code/config.json'

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked.')




    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned.')



    @commands.command(name='purge')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 100):
        """Purge a certain number of messages from the channel."""
        if limit > 1000:
            await ctx.send("You cannot delete more than 1000 messages at once.")
            return

        deleted = await ctx.channel.purge(limit=limit + 1)
        await ctx.send(f"Deleted {len(deleted) - 1} messages.")

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")




    @commands.command(name='setwelcome')
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, ctx: commands.Context, channel: discord.TextChannel):
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




    @commands.command(name='setleave')
    @commands.has_permissions(administrator=True)
    async def set_leave_channel(self, ctx: commands.Context, channel: discord.TextChannel):
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




    @commands.command(name='setverifiedrole')
    @commands.has_permissions(administrator=True)
    async def set_verified_role(self, ctx: commands.Context, role: discord.Role):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {}
        if 'roles' not in config[guild_id]:
            config[guild_id]['roles'] = {}
        config[guild_id]['roles']['verified'] = str(role.id)

        with open(config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f'Verified role has been set to {role.name}')




    @commands.command(name='addprohibited')
    @commands.has_permissions(administrator=True)
    async def add_prohibited_word(self, ctx: commands.Context, word: str):
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




    @commands.command(name='removeprohibited')
    @commands.has_permissions(administrator=True)
    async def remove_prohibited_word(self, ctx: commands.Context, word: str):
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




async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCommands(bot))
