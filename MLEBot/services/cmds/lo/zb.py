import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Zb(Cmd):
    """My link is borked, halp
    """
    @app_commands.command(name='zb',
                          description='My link is borked, halp')
    @app_commands.default_permissions()
    async def zb(self,
                 interaction: discord.Interaction):
        await interaction.response.send_message("https://tinyurl.com/rmblmv8")
