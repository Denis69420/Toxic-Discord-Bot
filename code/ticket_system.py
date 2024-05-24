import discord
from discord.ext import commands
from discord.ui import Button, View
from .localization import Localization
import json
import os

config_file_path = 'code/config.json'

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ticket System Cog is ready.")

    @commands.command(name='setticketchannel')
    @commands.has_permissions(administrator=True)
    async def set_ticket_channel(self, ctx, channel: discord.TextChannel):
        with open(config_file_path, 'r') as f:
            config = json.load(f)
        
        guild_id = str(ctx.guild.id)
        if guild_id not in config:
            config[guild_id] = {}

        config[guild_id]['ticket_channel_id'] = channel.id

        with open(config_file_path, 'w') as f:
            json.dump(config, f, indent=4)

        await ctx.send(f"Ticket channel has been set to {channel.mention}.")

    @commands.command(name='createticket')
    async def create_ticket(self, ctx):
        view = View()
        button = Button(label=Localization.get_message(ctx.guild.id, 'open_ticket'), style=discord.ButtonStyle.primary)
        button.callback = self.open_ticket
        view.add_item(button)
        await ctx.send(Localization.get_message(ctx.guild.id, 'ticket_create_prompt'), view=view)

    async def open_ticket(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        category = discord.utils.get(interaction.guild.categories, name="Tickets")
        if category is None:
            category = await interaction.guild.create_category("Tickets")

        ticket_channel = await interaction.guild.create_text_channel(f"ticket-{interaction.user.display_name}", category=category)
        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await ticket_channel.send(f"{interaction.user.mention}, {Localization.get_message(interaction.guild.id, 'ticket_open_message')}")

        close_button = Button(label=Localization.get_message(interaction.guild.id, 'close_ticket'), style=discord.ButtonStyle.danger)
        view = View()
        close_button.callback = self.close_ticket
        view.add_item(close_button)
        await ticket_channel.send(view=view)

    async def close_ticket(self, interaction: discord.Interaction):
        await interaction.channel.delete()

async def setup(bot: commands.Bot):
    await bot.add_cog(TicketSystem(bot))
