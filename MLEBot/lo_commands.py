#!/usr/bin/env python
""" Minor League E-Sports Bot League Operation Specific Commands
# Author: irox_rl
# Purpose: General Functions and Commands
# Version 1.0.6
#
# v1.0.6 - Include slash commands
"""

# local imports #

# non-local imports #
import discord
from discord import app_commands
from discord.ext import commands


class LoCommands(commands.Cog):
    def __init__(self,
                 master_bot):
        self.bot = master_bot

    @app_commands.command(name='achilles',
                          description='mr. worldwide')
    @app_commands.default_permissions()
    async def achilles(self,
                       interaction: discord.Interaction):
        await interaction.response.send_message("""https://media.discordapp.net/attachments/1101172529676161155/1257818646005415966/A_Chillis_tendon.png?ex=6685ca66&is=668478e6&hm=59e3c53b51b45477562b895acd641397a1144ebc5e690e6b4b875b9ca83c0ca0&=&format=webp&quality=lossless""")

    @app_commands.command(name='adi',
                          description='Brick by boring brick.')
    @app_commands.default_permissions()
    async def adi(self,
                  interaction: discord.Interaction):
        _bricks = [':brick:'] * 20
        await interaction.response.send_message(' '.join(_bricks))

    @app_commands.command(name='bw',
                          description='Galaxy brain.')
    @app_commands.default_permissions()
    async def bw(self,
                 interaction: discord.Interaction):
        await interaction.response.send_message('KISSEWDAKHTKISS')

    @app_commands.command(name='haim',
                          description='S(HAIM).')
    @app_commands.default_permissions()
    async def haim(self,
                   interaction: discord.Interaction):
        await interaction.response.send_message(
            'https://media.discordapp.net/attachments/670665177863028750/940985245786837022/ezgif.com-gif-maker_1.gif?ex=667cd58d&is=667b840d&hm=0f7548f793f01ec70d4a45093083e3c13310754eb3b7d07a4b78cfd1085c9405&=')

    @app_commands.command(name='hoos',
                          description=':kissing_heart:')
    @app_commands.default_permissions()
    async def hoos(self,
                   interaction: discord.Interaction):
        await interaction.response.send_message(
            'Friends share more DNA than strangers.')

    @app_commands.command(name='kd',
                          description='KD')
    @app_commands.default_permissions()
    async def kd(self,
                 interaction: discord.Interaction):
        await interaction.response.send_message(
            '` `')

    @app_commands.command(name='kunics',
                          description='PIVOT')
    @app_commands.default_permissions()
    async def kunics(self,
                     interaction: discord.Interaction):
        await interaction.response.send_message("""***P I V O T
I V O T
V O T
O T
T***""")

    @app_commands.command(name='maple',
                          description='Oh, Canada...')
    @app_commands.default_permissions()
    async def maple(self,
                    interaction: discord.Interaction):
        await interaction.response.send_message(':flag_ca: Sorry. :flag_ca:')

    @app_commands.command(name='ondo',
                          description='ondofir')
    @app_commands.default_permissions()
    async def ondo(self,
                   interaction: discord.Interaction):
        await interaction.response.send_message(
            'https://media.discordapp.net/attachments/532946038080798730/709472405914910840/unknown.png?ex=667d06ea&is=667bb56a&hm=968a10b7a304b47c14a13b4333766419a3ae24f4a8c809910d241ee57f1689f0&=&format=webp&quality=lossless')

    @app_commands.command(name='rexton',
                          description='opens door...')
    @app_commands.default_permissions()
    async def rexton(self,
                  interaction: discord.Interaction):
        await interaction.response.send_message('https://media.discordapp.net/attachments/832819833611223081/996629449242058852/image_15_1.png?ex=667ce601&is=667b9481&hm=d3c4f0f7ae0074167a828db9b5b6deb8681a2c7bf1b93e428187327a1e3cea9e&=&format=webp&quality=lossless&width=1179&height=619')

    @app_commands.command(name='riz',
                          description='@Riz')
    @app_commands.default_permissions()
    async def riz(self,
                  interaction: discord.Interaction):
        await interaction.response.send_message('neck')

    @app_commands.command(name='soviet',
                          description='Oh, the burning...')
    @app_commands.default_permissions()
    async def soviet(self,
                     interaction: discord.Interaction):
        await interaction.response.send_message("""***The Crucifixion of Morality***

*The Crucifixion of Morality is an image of 69 horseshoe crabmen and an alpaca. The alpaca is striking a menacing pose. The 69 horseshoe crabmen are burning. *
https://cdn.mlesports.dev/public/The_Crucifixion_of_Morality.png""")

    @app_commands.command(name='zb',
                          description='My link is borked, halp')
    @app_commands.default_permissions()
    async def zb(self,
                 interaction: discord.Interaction):
        await interaction.response.send_message("https://tinyurl.com/rmblmv8")
