"""@Riz
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Riz(Cog):
    """@Riz
    """

    @app_commands.command(name='riz',
                          description='@Riz')
    @app_commands.default_permissions()
    async def riz(self,
                  interaction: discord.Interaction):
        """@Riz
        """
        await interaction.response.send_message('neck')
