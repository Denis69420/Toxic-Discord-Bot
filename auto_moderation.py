import discord
from discord.ext import commands
import json
import os

config_file_path = 'code/config.json'

def setup(bot: commands.Bot):
    @bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return

        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(message.guild.id)
        prohibited_words = config.get(guild_id, {}).get('prohibited_words', [])

        if any(word in message.content.lower() for word in prohibited_words):
            await message.delete()
            await message.channel.send(f'{message.author.mention}, your message contained prohibited content and was deleted.', delete_after=10)

        await bot.process_commands(message)