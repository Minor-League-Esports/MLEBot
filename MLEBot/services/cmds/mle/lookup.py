"""Lookup player by MLE name.
    """

import discord
from discord import app_commands
from pydiscobot.types import Cmd
from ....embed_frames import salary_card
from ....services.const import ERR_BAD_NAME
from ...sprocket.lookup import lookup_rl
from ....types.member import Member


class Lookup(Cmd):
    """Lookup player by MLE name.
    """

    @app_commands.command(name='lookup',
                          description='Lookup player by MLE name.')
    @app_commands.describe(mle_name='Player name.')
    @app_commands.default_permissions()
    async def lookup(self,
                     interaction: discord.Interaction,
                     mle_name: str) -> None:
        'Lookup player by MLE name provided.'
        member: Member = lookup_rl(self._parent.sprocket.links,
                                   name=mle_name)
        if not member:
            self._parent.send_notification(interaction,
                                           ERR_BAD_NAME,
                                           as_reply=True)
            return
        await interaction.response.send_message(embed=salary_card(member))
