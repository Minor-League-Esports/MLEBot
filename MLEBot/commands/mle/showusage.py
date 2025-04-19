"""show play usage of players for a franchise.
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


from ...const import ERR_BAD_FRANCHISE
from ...frames import usage_card
from ...services.sprocket import lookup_franchise


class ShowUsage(Cog):
    """show play usage of players for a franchise.
    """

    @app_commands.command(name='showusage',
                          description='show play usage of players for a franchise.')
    @app_commands.default_permissions()
    async def showusage(self,
                        interaction: discord.Interaction) -> None:
        """show usage of members from a user's franchise

        Args:
            interaction (discord.Interaction): discord.Interaction
        """
        await interaction.response.defer()
        franchise = lookup_franchise(self._parent.sprocket.links,
                                     discord_id=interaction.user.id)
        if not franchise:
            await self._parent.send_notification(interaction,
                                                 ERR_BAD_FRANCHISE,
                                                 as_followup=True)
            return

        await interaction.followup.send(embed=usage_card(franchise))
