"""ondofir
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Ondo(Cog):
    """ondofir
    """

    @app_commands.command(name='ondo',
                          description='ondofir')
    @app_commands.default_permissions()
    async def ondo(self,
                   interaction: discord.Interaction):
        """ondofir
        """
        await interaction.response.send_message(
            'https://media.discordapp.net/attachments/532946038080798730/709472405914910840/unknown.png?ex=667d06ea&is=667bb56a&hm=968a10b7a304b47c14a13b4333766419a3ae24f4a8c809910d241ee57f1689f0&=&format=webp&quality=lossless')
