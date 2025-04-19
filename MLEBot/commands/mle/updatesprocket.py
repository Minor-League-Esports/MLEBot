"""Update info from sprocket.
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class UpdateSprocket(Cog):
    """Update info from sprocket.
    """

    @app_commands.command(name='updatesprocket',
                          description='Update info from sprocket.')
    @app_commands.default_permissions()
    async def updatesprocket(self,
                             interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        self._parent.sprocket.reset()
        await self._parent.sprocket.run()
        await self._parent.send_notification(interaction,
                                             'League-Sprocket update complete.',
                                             as_followup=True)
