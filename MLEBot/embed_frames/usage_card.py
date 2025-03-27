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


def usage_card(franchise: {},
               players: {}):
    embed = (discord.Embed(
        color=discord.Color.from_str(franchise['Primary Color']),
        title=f"**{franchise['Franchise']} Slot Usage Info**",
        description='Data gathered by sprocket public data links.\n'
                    'See more at [sprocket links](https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html)\n')
             .set_footer(text=f'Generated: {datetime.datetime.now()}'))
    embed.set_thumbnail(url=franchise['Photo URL'])

    embed.add_field(name='**Season Slot Allowances**',
                    value='`Doubles: 6 | Standard: 8 | Total: 12`   ',
                    inline=False)

    if players['PL']:
        embed.add_field(
            name='Premier',
            value='\n'.join([__player_usage_string__(x)
                            for x in players['PL']]),
            inline=False)

    if players['ML']:
        embed.add_field(
            name='Master',
            value='\n'.join([__player_usage_string__(x)
                            for x in players['ML']]),
            inline=False)

    if players['CL']:
        embed.add_field(
            name='Champion',
            value='\n'.join([__player_usage_string__(x)
                            for x in players['CL']]),
            inline=False)

    if players['AL']:
        embed.add_field(
            name='Academy',
            value='\n'.join([__player_usage_string__(x)
                            for x in players['AL']]),
            inline=False)

    if players['FL']:
        embed.add_field(
            name='Foundation',
            value='\n'.join([__player_usage_string__(x)
                            for x in players['FL']]),
            inline=False)

    return embed


def __player_usage_string__(player):
    return f"`{player['player']['slot'].removeprefix('PLAYER')} | 2s: {player['usage']['doubles_uses']} | 3s: {player['usage']['standard_uses']} | Total: {player['usage']['total_uses']} | {player['player']['name']}`"
