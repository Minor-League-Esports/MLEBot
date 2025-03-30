import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Riz(Cmd):
    """@Riz
    """

    @app_commands.command(name='riz',
                          description='@Riz')
    @app_commands.default_permissions()
    async def riz(self,
                  interaction: discord.Interaction):
        await interaction.response.send_message('neck')
