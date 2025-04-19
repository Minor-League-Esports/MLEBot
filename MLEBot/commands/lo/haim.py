"""S(HAIM).
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Haim(Cog):
    """S(HAIM).
    """

    @app_commands.command(name='haim',
                          description='S(HAIM).')
    @app_commands.default_permissions()
    async def haim(self,
                   interaction: discord.Interaction):
        """S(HAIM).
        """
        await interaction.response.send_message(
            'https://media.discordapp.net/attachments/670665177863028750/940985245786837022/ezgif.com-gif-maker_1.gif?ex=667cd58d&is=667b840d&hm=0f7548f793f01ec70d4a45093083e3c13310754eb3b7d07a4b78cfd1085c9405&=')
