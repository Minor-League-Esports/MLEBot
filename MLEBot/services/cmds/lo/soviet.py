"""Oh, the burning...
    """

import discord
from discord import app_commands
from pydiscobot.types import Cmd


class Soviet(Cmd):
    """Oh, the burning...
    """

    @app_commands.command(name='soviet',
                          description='Oh, the burning...')
    @app_commands.default_permissions()
    async def soviet(self,
                     interaction: discord.Interaction):
        """Oh, the burning...
        """
        await interaction.response.send_message("""***The Crucifixion of Morality***
*The Crucifixion of Morality is an image of 69 horseshoe crabmen and an alpaca. The alpaca is striking a menacing pose. The 69 horseshoe crabmen are burning. *
https://cdn.mlesports.dev/public/The_Crucifixion_of_Morality.png""")
