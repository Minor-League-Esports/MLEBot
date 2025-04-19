"""My link is borked, halp
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Zb(Cog):
    """My link is borked, halp
    """
    @app_commands.command(name='zb',
                          description='My link is borked, halp')
    @app_commands.default_permissions()
    async def zb(self,
                 interaction: discord.Interaction):
        """My link is borked, halp
        """
        await interaction.response.send_message("https://tinyurl.com/rmblmv8")
