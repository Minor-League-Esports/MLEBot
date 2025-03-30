import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Adi(Cmd):
    """Brick by boring brick.
    """

    @app_commands.command(name='adi',
                          description='Brick by boring brick.')
    @app_commands.default_permissions()
    async def adi(self,
                  interaction: discord.Interaction):
        _bricks = [':brick:'] * 20
        await interaction.response.send_message(' '.join(_bricks))