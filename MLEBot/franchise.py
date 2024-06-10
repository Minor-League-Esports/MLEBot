#!/usr/bin/env python
""" Minor League E-Sports Franchise
# Author: irox_rl
# Purpose: General Functions of a League Franchise
# Version 1.0.2
"""

# local imports #
from MLEBot.enums import *
from MLEBot.member import Member
from MLEBot.team import Team

# non-local imports #
import discord
from discord.ext import commands
import os


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

    async def post_player_quick_info(self,
                                     player: discord.Member,
                                     ctx: discord.ext.commands.Context):
        _member = Member(player)
        await _member.__build_from_sprocket__(self.bot.sprocket.data)
        await _member.post_quick_info(ctx)

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

    async def rebuild(self) -> str:
        """ rebuild franchise\n
            ***param members***: list of members to build from\n
            ***returns***: status string\n
        """
        if not self.premier_disabled:
            self.premier_league = Team(self.guild, self, LeagueEnum.Premier_League)
        self.master_league = Team(self.guild, self, LeagueEnum.Master_League)
        self.champion_league = Team(self.guild, self, LeagueEnum.Champion_League)
        self.academy_league = Team(self.guild, self, LeagueEnum.Academy_League)
        if not self.foundation_disabled:
            self.foundation_league = Team(self.guild, self, LeagueEnum.Foundation_League)
        await self.build()
        return 'Userbase has been successfully rebuilt!'
