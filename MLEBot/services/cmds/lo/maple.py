import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Maple(Cmd):
    """Oh, Canada...
    """

    @app_commands.command(name='maple',
                          description='Oh, Canada...')
    @app_commands.default_permissions()
    async def maple(self,
                    interaction: discord.Interaction):
        await interaction.response.send_message(':flag_ca: Sorry. :flag_ca:')
