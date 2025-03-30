import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Hoos(Cmd):
    """:kissing_heart:
    """

    @app_commands.command(name='hoos',
                          description=':kissing_heart:')
    @app_commands.default_permissions()
    async def hoos(self,
                   interaction: discord.Interaction):
        await interaction.response.send_message(
            'Friends share more DNA than strangers.')
