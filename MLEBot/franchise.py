#!/usr/bin/env python
""" Minor League E-Sports Franchise
# Author: irox_rl
# Purpose: General Functions of a League Franchise
# Version 1.0.6
#
# v1.0.6 - include salary caps until sprocket does.
"""

# local imports #
from MLEBot.enums import *
from MLEBot.member import Member
from MLEBot.team import Team

# non-local imports #
import discord
from discord.ext import commands
import os

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
                 disable_premier_league: bool = False,
                 disable_foundation_league: bool = False) -> None:
        """ Initialize method\n
                    **param guild**: reference to guild this franchise belongs to\n
                    **param team_name**: string representation of this team's name (e.g. **'Sabres'**)\n
                    **param team_name**: asynchronous callback method for status updates\n
                    All data is initialized to zero. Franchise load will be called 'on_ready' of the bot
                """
        self.bot = master_bot
        self.guild = guild
        self.franchise_name = os.getenv('TEAM_NAME')
        self.premier_league = Team(self.guild,
                                   self,
                                   LeagueEnum.Premier_League) if not disable_premier_league else None
        self.premier_disabled = True if self.premier_league is None else False
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
                                      LeagueEnum.Foundation_League) if not disable_foundation_league else None
        self.foundation_disabled = True if self.foundation_league is None else False

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

    def add_member(self,
                   _member: Member) -> bool:
        """ add member to this franchise. Will be delegated based on **member.league**\n
                **param member**: MLE Member to be added to this franchise (welcome!)\n
                **returns** delegated success returned from the team's add method
                """
        """ Match the league and return its' return 
        """
        match _member.league:
            case LeagueEnum.Premier_League:
                if not self.premier_disabled:
                    return self.premier_league.add_member(_member)
                else:
                    return False
            case LeagueEnum.Master_League:
                return self.master_league.add_member(_member)
            case LeagueEnum.Champion_League:
                return self.champion_league.add_member(_member)
            case LeagueEnum.Academy_League:
                return self.academy_league.add_member(_member)
            case LeagueEnum.Foundation_League:
                if not self.foundation_disabled:
                    return self.foundation_league.add_member(_member)
                else:
                    return False
        return False

    async def build(self) -> None:
        """ build member-base from list of members\n
                        **returns**: None
                        """
        for mem in self.guild.members:
            league_member = Member(mem)
            if league_member.league:
                self.add_member(league_member)

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
            _players = None
        return sorted(_players, key=lambda x: x.role)

    async def init(self,
                   guild: discord.Guild):
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
        if not guild:
            raise KeyError('MLE Team needs to have a reference to its own guild')
        self.guild = guild
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
        if not self.premier_disabled:
            self.premier_league = Team(self.guild, self, LeagueEnum.Premier_League)
        self.master_league = Team(self.guild, self, LeagueEnum.Master_League)
        self.champion_league = Team(self.guild, self, LeagueEnum.Champion_League)
        self.academy_league = Team(self.guild, self, LeagueEnum.Academy_League)
        if not self.foundation_disabled:
            self.foundation_league = Team(self.guild, self, LeagueEnum.Foundation_League)
        await self.build()
