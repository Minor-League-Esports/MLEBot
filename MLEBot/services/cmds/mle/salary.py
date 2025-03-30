import discord
from discord import app_commands
from pydiscobot.services.cmds._cmd import Cmd
from ....embed_frames import salary_card
from ....services.const import ERR_BAD_NAME
from ...sprocket.lookup import lookup_rl
from ....types.member import Member


class Salary(Cmd):
    """Lookup player by MLE name.
    """

    @app_commands.command(name='salary',
                          description='Lookup your salary card.')
    @app_commands.default_permissions()
    async def lookup(self,
                     interaction: discord.Interaction,):
        'Lookup player by MLE name provided.'
        member: Member = lookup_rl(self._parent.sprocket.links,
                                   discord_id=interaction.user.id)
        if not member:
            self._parent.send_notification(interaction,
                                           ERR_BAD_NAME,
                                           as_reply=True)
            return
        await interaction.response.send_message(embed=salary_card(member))
