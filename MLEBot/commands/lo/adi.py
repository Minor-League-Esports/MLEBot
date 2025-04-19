"""Brick by boring brick.
    """
from __future__ import annotations


import discord
from discord import app_commands


from pydiscobot import Cog


class Adi(Cog):
    """Brick by boring brick.
    """

    @app_commands.command(name='adi',
                          description='Brick by boring brick.')
    @app_commands.default_permissions()
    async def adi(self,
                  interaction: discord.Interaction):
        """Brick by boring brick.
        """
        _bricks = [':brick:'] * 20
        await interaction.response.send_message(' '.join(_bricks))
