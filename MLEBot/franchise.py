#!/usr/bin/env python
""" Minor League E-Sports Franchise
# Author: irox_rl
# Purpose: General Functions of a League Franchise
# Version 1.0.6
#
# v1.0.6 - include salary caps until sprocket does.
"""

# local imports #
from enums import *
from team import Team

# non-local imports #
import discord
from discord.ext import commands

# constants
SALARY_CAP_PL = 95.0
SALARY_CAP_ML = 82.0
SALARY_CAP_CL = 69.5
SALARY_CAP_AL = 57.5
SALARY_CAP_FL = 39.5


class Franchise:
    """ Minor League E-Sports Discord Franchise
        This class houses all leagues associated with a franchise
        """

    def __init__(self,
                 master_bot,
                 guild: discord.Guild,
                 franchise_name: str) -> None:
        """ Initialize method\n
                    **param guild**: reference to guild this franchise belongs to\n
                    **param team_name**: string representation of this team's name (e.g. **'Sabres'**)\n
                    **param team_name**: asynchronous callback method for status updates\n
                    All data is initialized to zero. Franchise load will be called 'on_ready' of the bot
                """
        self.bot = master_bot
        self.guild = guild
        self.franchise_name = franchise_name
        self.premier_league = Team(self.guild,
                                   self,
                                   LeagueEnum.Premier_League)
        self.master_league = Team(self.guild,
                                  self,
                                  LeagueEnum.Master_League)
        self.champion_league = Team(self.guild,
                                    self,
                                    LeagueEnum.Champion_League)
        self.academy_league = Team(self.guild,
                                   self,
                                   LeagueEnum.Academy_League)
        self.foundation_league = Team(self.guild,
                                      self,
                                      LeagueEnum.Foundation_League)
        self._sprocket_team: {} = None
        self._sprocket_members: [{}] = []
        self._sprocket_players: [{}] = []

    @property
    def all_members(self) -> [[],
                              [],
                              [],
                              [],
                              []]:
        """ return a list containing all lists of members from each team in the franchise
                        """
        lst = []
        for _team in self.teams:
            lst.extend(_team.players)
        return lst

    @property
    def sprocket_team(self):
        return self._sprocket_team

    @property
    def sprocket_members(self):
        return self._sprocket_members

    @property
    def sprocket_players(self):
        return self._sprocket_players

    @property
    def teams(self) -> [Team]:
        lst = []
        if self.premier_league:
            lst.append(self.premier_league)
        if self.master_league:
            lst.append(self.master_league)
        if self.champion_league:
            lst.append(self.champion_league)
        if self.academy_league:
            lst.append(self.academy_league)
        if self.foundation_league:
            lst.append(self.foundation_league)
        return lst

    def build_sprocket_data(self):
        self._sprocket_team = next((x for x in self.bot.sprocket.data['sprocket_teams'] if self.franchise_name == x['name']), None)
        self._sprocket_players = [x for x in self.bot.sprocket.data['sprocket_players'] if x['franchise'] == self.franchise_name]
        self._sprocket_members = []
        for _player in self.sprocket_players:
            _mem = next(
                (x for x in self.bot.sprocket.data['sprocket_members'] if x['member_id'] == _player['member_id']), None)
            if _mem:
                self._sprocket_members.append(_mem)

    async def get_team_eligibility(self,
                                   team: LeagueEnum):
        if team == LeagueEnum.Premier_League and self.premier_league:
            _players = await self.premier_league.get_updated_players()
        elif team == LeagueEnum.Master_League and self.master_league:
            _players = await self.master_league.get_updated_players()
        elif team == LeagueEnum.Champion_League and self.champion_league:
            _players = await self.champion_league.get_updated_players()
        elif team == LeagueEnum.Academy_League and self.academy_league:
            _players = await self.academy_league.get_updated_players()
        elif team == LeagueEnum.Foundation_League and self.foundation_league:
            _players = await self.foundation_league.get_updated_players()
        else:
            return None
        return sorted(_players, key=lambda x: x.role)

    async def init(self):
        """ initialization method\n
        **`optional`param sprocket_delegate**: sprocket method delegate that we can append internally\n
        **`optional`param premier_channel**: channel to post quick info\n
        **`optional`param master_channel**: channel to post quick info\n
        **`optional`param champion_channel**: channel to post quick info\n
        **`optional`param academy_channel**: channel to post quick info\n
        **`optional`param foundation_channel**: channel to post quick info\n
        **returns**: status string of the init method\n
            """
        """ check if our method is in delegate, then add
                """
        """ assign datas locally
        """
        await self.rebuild()

    async def post_season_stats_html(self,
                                     league: str,
                                     ctx: discord.ext.commands.Context | discord.TextChannel | None = None):
        _league = next((x for x in self.teams if league in x.league_name.lower()), None)
        if not _league:
            await self.bot.send_notification(ctx,
                                             f'{league} was not a valid league name!',
                                             True)
        await _league.post_season_stats_html('Standard',
                                             ctx)
        await _league.post_season_stats_html('Doubles',
                                             ctx)

    async def rebuild(self) -> None:
        """ rebuild franchise
        """
        self.build_sprocket_data()
        self.premier_league = Team(self.guild, self, LeagueEnum.Premier_League)
        self.master_league = Team(self.guild, self, LeagueEnum.Master_League)
        self.champion_league = Team(self.guild, self, LeagueEnum.Champion_League)
        self.academy_league = Team(self.guild, self, LeagueEnum.Academy_League)
        self.foundation_league = Team(self.guild, self, LeagueEnum.Foundation_League)
        self.premier_league.build()
        self.master_league.build()
        self.champion_league.build()
        self.academy_league.build()
        self.foundation_league.build()
