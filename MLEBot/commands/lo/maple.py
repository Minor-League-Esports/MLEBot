"""Oh, Canada...
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Maple(Cog):
    """Oh, Canada...
    """

    @app_commands.command(name='maple',
                          description='Oh, Canada...')
    @app_commands.default_permissions()
    async def maple(self,
                    interaction: discord.Interaction):
        """Oh, Canada...
        """
        await interaction.response.send_message(':flag_ca: Sorry. :flag_ca:')
