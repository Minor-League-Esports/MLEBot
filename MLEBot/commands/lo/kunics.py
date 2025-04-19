"""PIVOT
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Kunics(Cog):
    """PIVOT
    """

    @app_commands.command(name='kunics',
                          description='PIVOT')
    @app_commands.default_permissions()
    async def kunics(self,
                     interaction: discord.Interaction):
        """PIVOT
        """
        await interaction.response.send_message("""***P I V O T
I V O T
V O T
O T
T***""")
