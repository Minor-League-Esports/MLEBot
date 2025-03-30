import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Kunics(Cmd):
    """PIVOT
    """

    @app_commands.command(name='kunics',
                          description='PIVOT')
    @app_commands.default_permissions()
    async def kunics(self,
                     interaction: discord.Interaction):
        await interaction.response.send_message("""***P I V O T
I V O T
V O T
O T
T***""")
