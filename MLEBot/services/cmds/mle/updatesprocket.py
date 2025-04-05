"""Update info from sprocket.
    """

import discord
from discord import app_commands
from pydiscobot.types import Cmd


class UpdateSprocket(Cmd):
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
