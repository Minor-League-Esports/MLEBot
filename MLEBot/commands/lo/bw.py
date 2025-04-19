"""Galaxy brain
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Bw(Cog):
    """Galaxy brain
    """

    @app_commands.command(name='bw',
                          description='Galaxy brain.')
    @app_commands.default_permissions()
    async def bw(self,
                 interaction: discord.Interaction):
        """Galaxy brain
        """
        await interaction.response.send_message('KISSEWDAKHTKISS')
