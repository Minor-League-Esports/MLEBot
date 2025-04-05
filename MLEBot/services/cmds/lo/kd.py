"""KD
    """

import discord
from discord import app_commands
from pydiscobot.types import Cmd


class Kd(Cmd):
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
