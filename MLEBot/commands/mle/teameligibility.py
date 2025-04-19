"""Show team eligibility.
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


from ... import const
from ...frames import teameligibility_card
from ...types import Franchise
from ...services.sprocket import lookup_franchise


class TeamEligibility(Cog):
    """Show team eligibility.
    """

    @app_commands.command(name='teameligibility',
                          description='Show team eligibility.')
    @app_commands.describe(league='[PL, ML, CL, AL, FL]')
    @app_commands.choices(league=[
        app_commands.Choice(name='PL', value=const.SPR_SG_PL),
        app_commands.Choice(name='ML', value=const.SPR_SG_ML),
        app_commands.Choice(name='CL', value=const.SPR_SG_CL),
        app_commands.Choice(name='AL', value=const.SPR_SG_AL),
        app_commands.Choice(name='FL', value=const.SPR_SG_FL)
    ])
    @app_commands.default_permissions()
    async def teameligibility(self,
                              interaction: discord.Interaction,
                              league: app_commands.Choice[str]) -> None:
        """get team eligibility

        Args:
            interaction (discord.Interaction): discord interaction
            league (app_commands.Choice[str]): which league to display
        """
        await interaction.response.defer()
        franchise: Franchise = lookup_franchise(self._parent.sprocket.links,
                                                discord_id=interaction.user.id)
        if not franchise:
            await self._parent.send_notification(interaction,
                                                 const.ERR_BAD_FRANCHISE,
                                                 as_followup=True)
            return

        await interaction.followup.send(embed=teameligibility_card(franchise,
                                                                   league.value))
