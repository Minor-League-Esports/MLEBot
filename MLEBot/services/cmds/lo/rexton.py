import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Rexton(Cmd):
    """opens door...
    """

    @app_commands.command(name='rexton',
                          description='opens door...')
    @app_commands.default_permissions()
    async def rexton(self,
                     interaction: discord.Interaction):
        await interaction.response.send_message('https://media.discordapp.net/attachments/832819833611223081/996629449242058852/image_15_1.png?ex=667ce601&is=667b9481&hm=d3c4f0f7ae0074167a828db9b5b6deb8681a2c7bf1b93e428187327a1e3cea9e&=&format=webp&quality=lossless&width=1179&height=619')
