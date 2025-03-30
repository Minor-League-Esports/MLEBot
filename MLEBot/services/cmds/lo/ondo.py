import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Ondo(Cmd):
    """ondofir
    """

    @app_commands.command(name='ondo',
                          description='ondofir')
    @app_commands.default_permissions()
    async def ondo(self,
                   interaction: discord.Interaction):
        await interaction.response.send_message(
            'https://media.discordapp.net/attachments/532946038080798730/709472405914910840/unknown.png?ex=667d06ea&is=667bb56a&hm=968a10b7a304b47c14a13b4333766419a3ae24f4a8c809910d241ee57f1689f0&=&format=webp&quality=lossless')
