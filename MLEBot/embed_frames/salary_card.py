#!/usr/bin/env python
""" Minor League E-Sports Rocket League Player Salary Card
# Author: irox_rl
# Purpose: Salary Card embed function for ease of access / cleanliness
# Version 1.0.7
#
# v1.0.7 - init
"""
import datetime
import discord
import os


def salary_card(member: {},
                player: {},
                franchise: {},
                player_tracker: {}):
    embed = (discord.Embed(
        color=discord.Color.from_str(
            franchise['Primary Color']) if franchise else discord.Color.from_str(os.getenv('MLE_COLOR')),
        title=f"**{member['name']} Sprocket Info**",
        description='Data gathered by sprocket public data links.\n'
                    'See more at [sprocket links](https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html)\n')
        .set_footer(text=f'Generated: {datetime.datetime.now()}'))
    embed.set_thumbnail(url=os.getenv('MLE_LOGO_URL')
                        if not franchise else franchise['Photo URL'])
    embed.add_field(name='MLE Name', value=f"`{member['name']}`", inline=True)
    embed.add_field(name='MLE ID', value=f"`{member['mle_id']}`", inline=True)
    embed.add_field(name='Salary', value=f"`{player['salary']}`", inline=True)
    embed.add_field(
        name='League', value=f"`{player['skill_group']}`", inline=True)
    embed.add_field(name='Scrim Points',
                    value=f"`{player['current_scrim_points']}`", inline=True)
    embed.add_field(
        name='Eligible?', value="`Yes`" if player['current_scrim_points'] >= 30 else "`No`", inline=True)
    embed.add_field(name='Franchise',
                    value=f"`{player['franchise']}`", inline=True)
    embed.add_field(name='Staff Position',
                    value=f"`{player['Franchise Staff Position']}`", inline=True)
    embed.add_field(name='Role', value=f"`{player['slot']}`", inline=True)
    if player_tracker:
        embed.add_field(name='**Tracker Link**',
                        value=player_tracker['tracker'], inline=False)
    return embed
