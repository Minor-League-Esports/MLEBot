from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


from ...const import ERR_BAD_FRANCHISE
from ...frames import teaminfo_card
from ...services.sprocket import lookup_franchise
from ...types import Franchise


class TeamInfo(Cog):
    """Get info about a team.
    """

    @app_commands.command(name='teaminfo',
                          description='Get info about a team.')
    @app_commands.describe(team_name='MLE Team to get info about.')
    @app_commands.default_permissions()
    async def teaminfo(self,
                       interaction: discord.Interaction,
                       team_name: str):
        """Get info about a team.
        """
        await interaction.response.defer()
        franchise: Franchise = lookup_franchise(self._parent.sprocket.links,
                                                name=team_name)
        if not franchise:
            await self._parent.send_notification(interaction,
                                                 ERR_BAD_FRANCHISE,
                                                 as_followup=True)
            return

        await interaction.followup.send(embed=teaminfo_card(franchise))
