""":kissing_heart:
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Hoos(Cog):
    """:kissing_heart:
    """

    @app_commands.command(name='hoos',
                          description=':kissing_heart:')
    @app_commands.default_permissions()
    async def hoos(self,
                   interaction: discord.Interaction):
        """:kissing_heart:
        """
        await interaction.response.send_message(
            'Friends share more DNA than strangers.')
