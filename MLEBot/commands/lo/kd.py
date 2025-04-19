"""KD
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Kd(Cog):
    """KD
    """

    @app_commands.command(name='kd',
                          description='KD')
    @app_commands.default_permissions()
    async def kd(self,
                 interaction: discord.Interaction):
        """KD
        """
        await interaction.response.send_message('` `')
