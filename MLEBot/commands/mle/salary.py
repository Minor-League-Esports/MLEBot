"""Show player salary.
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


from ...const import ERR_BAD_NAME
from ...frames import salary_card
from ...services.sprocket import lookup_rl
from ...types import Member


class Salary(Cog):
    """Show player salary.
    """

    @app_commands.command(name='salary',
                          description='Lookup your salary card.')
    @app_commands.default_permissions()
    async def lookup(self,
                     interaction: discord.Interaction) -> None:
        'Show player salary.'
        member: Member = lookup_rl(self._parent.sprocket.links,
                                   discord_id=interaction.user.id)
        if not member:
            await self._parent.send_notification(interaction,
                                                 ERR_BAD_NAME,
                                                 as_reply=True)
            return
        await interaction.response.send_message(embed=salary_card(member))
