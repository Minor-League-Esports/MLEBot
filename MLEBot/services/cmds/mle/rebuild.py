import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd


class Rebuild(Cmd):
    """Rebuild bot meta data.
    """

    @app_commands.command(name='rebuild',
                          description='Rebuild bot meta data.')
    @app_commands.guilds(1043295434828947547)
    @app_commands.default_permissions()
    async def rebuild(self,
                      interaction: discord.Interaction):
        """Rebuild bot meta data."""
        await interaction.response.defer()
        if await self._parent.rebuild():
            await self._parent.send_notification(interaction,
                                                 'Success!.',
                                                 as_followup=True)
        else:
            await self._parent.send_notification(interaction,
                                                 'An error has occured.',
                                                 as_followup=True)
