import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Bw(Cmd):
    """mr. worldwide
    """

    @app_commands.command(name='bw',
                          description='Galaxy brain.')
    @app_commands.default_permissions()
    async def bw(self,
                 interaction: discord.Interaction):
        await interaction.response.send_message('KISSEWDAKHTKISS')