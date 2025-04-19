"""Lookup player by MLE name.
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


from ...const import ERR_BAD_NAME
from ...frames import salary_card
from ...services.sprocket import lookup_rl
from ...types import Member


class Lookup(Cog):
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
            await self._parent.send_notification(interaction,
                                                 ERR_BAD_NAME,
                                                 as_reply=True)
            return
        await interaction.response.send_message(embed=salary_card(member))
