"""mr. worldwide
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Achilles(Cog):
    """mr. worldwide
    """

    @app_commands.command(name='achilles',
                          description='mr. worldwide')
    @app_commands.default_permissions()
    async def achilles(self,
                       interaction: discord.Interaction):
        """mr. worldwide"""
        await interaction.response.send_message("""https://media.discordapp.net/attachments/1101172529676161155/1257818646005415966/A_Chillis_tendon.png?ex=6685ca66&is=668478e6&hm=59e3c53b51b45477562b895acd641397a1144ebc5e690e6b4b875b9ca83c0ca0&=&format=webp&quality=lossless""")
