#!/usr/bin/env python
""" Periodic Task - Role
# Author: irox_rl
# Purpose: Manage roles of a franchise and roster channel information
# Version 1.0.2
"""

from PyDiscoBot import channels, err

# local imports #
from member import get_members_by_role
import roles

# non-local imports #
import datetime
import discord
from discord.ext import commands
import os
import pickle
from typing import Callable

IMG_STAFF = None
IMG_PREMIER = None
IMG_MASTER = None
IMG_CHAMPION = None
IMG_ACADEMY = None
IMG_FOUNDATION = None


class Task_Roster:
    def __init__(self,
                 master_bot):
        self.bot = master_bot

    def __get_league__(self,
                       _team: {},
                       _team_players: {},
                       _league: str,
                       _guild: discord.Guild) -> discord.Embed | None:
        embed = (discord.Embed(color=discord.Color.from_str(_team['primary_color']),
                               title=f"**{_league}**")
                 .set_footer(text=f'Generated: {self.bot.last_time}'))
        embed.set_thumbnail(url=_team['logo_img_link'])
        _players = [x for x in _team_players if x['skill_group'] == _league and x['slot'] != 'NONE']

        if len(_players) == 0:
            return None

        _player_mentions: [str] = []
        for _player in _players:
            _member = next((x for x in self.bot.sprocket.data['sprocket_members'] if x['member_id'] == _player['member_id']), None)
            if not _member:
                _player_mentions.append(_player['name'])
                continue
            _discord_member = next((x for x in _guild.members if x.id.__str__() == str(_member['discord_id'])), None)
            if not _discord_member:
                _player_mentions.append(_player['name'])
                continue
            _player_mentions.append(_discord_member.mention)

        if _player_mentions:
            embed.description = '\n'.join([x for x in _player_mentions if x is not None])
            return embed
        else:
            return None

    async def post_roster(self,
                          _team: {},
                          _channel: discord.TextChannel) -> bool:

        success = await channels.clear_channel_messages(_channel,
                                                        100)
        if not success:
            await err('Could not delete messages from roster channel!\n'
                      'Please manually delete them and retry running the ub.runroster command again.')
            return False

        _team_players = [x for x in self.bot.sprocket.data['sprocket_players'] if x['franchise'] == _team['name']]
        if not _team_players:
            await err('Could not find players for franchise!')
            return False

        _fm = next((x for x in _team_players if x['Franchise Staff Position'] == 'Franchise Manager'), None)
        _gms = [x for x in _team_players if x['Franchise Staff Position'] == 'General Manager']
        _agms = [x for x in _team_players if x['Franchise Staff Position'] == 'Assistant General Manager']
        _captains = [x for x in _team_players if x['Franchise Staff Position'] == 'Captain']
        _pr_supports = [x for x in _team_players if x['Franchise Staff Position'] == 'PR Support']

        embed = (discord.Embed(color=discord.Color.from_str(_team['primary_color']),
                               title=f"**{_team['name']} Staff**")
                 .set_footer(text=f'Generated: {self.bot.last_time}'))
        embed.set_thumbnail(url=_team['logo_img_link'])

        if _fm:
            _fm_text: str = ''
            _fm_member = next((x for x in self.bot.sprocket.data['sprocket_members'] if x['member_id'] == _fm['member_id']), None)
            if not _fm_member:
                _fm_text = _fm['name']
            else:
                _discord_mem = next((x for x in _channel.guild.members if x.id.__str__() == str(_fm_member['discord_id'])), None)
                if not _discord_mem:
                    _fm_text = _fm['name']
                else:
                    _fm_text = _discord_mem.mention
            embed.add_field(name='**Franchise Manager**',
                            value=_fm_text,
                            inline=True)

        if _gms:
            _gm_text: [str] = []
            for _gm in _gms:
                _gm_member = next((x for x in self.bot.sprocket.data['sprocket_members'] if x['member_id'] == _gm['member_id']), None)
                if not _gm_member:
                    _gm_text.append(_gm['name'])
                else:
                    _discord_mem = next((x for x in _channel.guild.members if x.id.__str__() == str(_gm_member['discord_id'])), None)
                    if not _discord_mem:
                        _gm_text.append(_gm['name'])
                    else:
                        _gm_text.append(_discord_mem.mention)
            embed.add_field(name='**General Managers**',
                            value='\n'.join(_gm_text),
                            inline=True)

        if _agms:
            _agm_text: [str] = []
            for _agm in _agms:
                _agm_member = next(
                    (x for x in self.bot.sprocket.data['sprocket_members'] if x['member_id'] == _agm['member_id']), None)
                if not _agm_member:
                    _agm_text.append(_agm['name'])
                else:
                    _discord_mem = next(
                        (x for x in _channel.guild.members if x.id.__str__() == str(_agm_member['discord_id'])), None)
                    if not _discord_mem:
                        _agm_text.append(_agm['name'])
                    else:
                        _agm_text.append(_discord_mem.mention)
            embed.add_field(name='**Assistant General Managers**',
                            value='\n'.join(_agm_text),
                            inline=True)

        if _captains:
            _captains_text: [str] = []
            for _captain in _captains:
                _captain_member = next(
                    (x for x in self.bot.sprocket.data['sprocket_members'] if x['member_id'] == _captain['member_id']),
                    None)
                if not _captain_member:
                    _captains_text.append(_captain['name'])
                else:
                    _discord_mem = next(
                        (x for x in _channel.guild.members if x.id.__str__() == str(_captain_member['discord_id'])), None)
                    if not _discord_mem:
                        _captains_text.append(_captain['name'])
                    else:
                        _captains_text.append(_discord_mem.mention)
            embed.add_field(name='**Captains**',
                            value='\n'.join(_captains_text),
                            inline=True)

        if _pr_supports:
            _text: [str] = []
            for _pr_support in _pr_supports:
                _pr_support_member = next(
                    (x for x in self.bot.sprocket.data['sprocket_members'] if x['member_id'] == _pr_support['member_id']),
                    None)
                if not _pr_support_member:
                    _text.append(_pr_support['name'])
                else:
                    _discord_mem = next(
                        (x for x in _channel.guild.members if x.id.__str__() == str(_pr_support_member['discord_id'])),
                        None)
                    if not _discord_mem:
                        _text.append(_pr_support['name'])
                    else:
                        _text.append(_discord_mem.mention)
            embed.add_field(name='**PR Supports**',
                            value='\n'.join(_text),
                            inline=True)

        await _channel.send(embed=embed)

        emb = self.__get_league__(_team,
                                  _team_players,
                                  'Premier League',
                                  _channel.guild)
        if emb:
            await _channel.send(embed=emb)

        emb = self.__get_league__(_team,
                                  _team_players,
                                  'Master League',
                                  _channel.guild)
        if emb:
            await _channel.send(embed=emb)

        emb = self.__get_league__(_team,
                                  _team_players,
                                  'Champion League',
                                  _channel.guild)
        if emb:
            await _channel.send(embed=emb)

        emb = self.__get_league__(_team,
                                  _team_players,
                                  'Academy League',
                                  _channel.guild)
        if emb:
            await _channel.send(embed=emb)

        emb = self.__get_league__(_team,
                                  _team_players,
                                  'Foundation League',
                                  _channel.guild)
        if emb:
            await _channel.send(embed=emb)
        # await channels.post_image(context, IMG_STAFF) if IMG_STAFF else None
        return True
