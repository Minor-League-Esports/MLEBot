#!/usr/bin/env python
""" Minor League E-Sports Member
# Author: irox_rl
# Purpose: General Functions of a League Member
# Version 1.0.4
"""

# local imports #
from MLEBot.enums import LeagueEnum
import MLEBot.roles

# non-local imports #
import discord
from discord.ext import commands


class Member:
    """ Minor League E-Sports Member
    """
    def __init__(self,
                 discord_member: discord.Member | None):
        """ Initiate member with reference to parent bot and discord.Member
            Other attributes are initialized to None or equivalent
            Members support saving and loading """
        self.discord_member: discord.Member = discord_member
        self.league: LeagueEnum | None = self.__get_league_role__(self.discord_member) if self.discord_member else None
        self.mle_name: str | None = None
        self.mle_id = None
        self.mle_player_id = None
        self.member_id = None
        self.sprocket_id = None
        self.schedule_confirmed = False
        self.salary = None
        self.scrim_points = None
        self.eligible = False
        self.role = None
        self.dpi = 0.0
        self.gpi = 0.0
        self.opi = 0.0
        self.goals = 0.0
        self.saves = 0.0
        self.score = 0.0
        self.shots = 0.0
        self.assists = 0.0
        self.goals_against = 0.0
        self.shots_against = 0.0

    def __eq__(self,
               other):
        if self.discord_member and other.discord_member:
            if self.discord_member == other.discord_member:
                return True
        if self.mle_id and other.mle_id:
            if self.mle_id == other.mle_id:
                return True
        if self.sprocket_id and other.sprocket_id:
            if self.sprocket_id == other.sprocket_id:
                return True
        return False

    @staticmethod
    def __get_league_role__(member: discord.Member) -> LeagueEnum | None:
        """ Returns league enumeration if user has associated role
            else returns None """
        for role in member.roles:
            if role.name == MLEBot.roles.PREMIER_LEAGUE:
                return LeagueEnum.Premier_League
            if role.name == MLEBot.roles.MASTER_LEAGUE:
                return LeagueEnum.Master_League
            if role.name == MLEBot.roles.CHAMPION_LEAGUE:
                return LeagueEnum.Champion_League
            if role.name == MLEBot.roles.ACADEMY_LEAGUE:
                return LeagueEnum.Academy_League
            if role.name == MLEBot.roles.FOUNDATION_LEAGUE:
                return LeagueEnum.Foundation_League

    async def __update_from_sprocket_players__(self,
                                               sprocket_players: {}) -> None:
        """ Update sprocket_id from sprocket_players.json data from sprocket database """
        if not sprocket_players:
            return
        player = next((x for x in sprocket_players if x['member_id'] == self.member_id), None)
        if not player:
            return
        self.sprocket_id = player['member_id']
        self.salary = player['salary']
        self.role = player['slot']
        self.scrim_points = player['current_scrim_points']
        self.eligible = True if self.scrim_points >= 30 else False

    async def __update_from_sprocket_player_stats__(self,
                                                    sprocket_player_stats):
        if not sprocket_player_stats:
            return
        player_stats = next((x for x in sprocket_player_stats if x['member_id'] == self.member_id), None)
        if not player_stats:
            return
        self.dpi = player_stats['dpi']
        self.gpi = player_stats['gpi']
        self.opi = player_stats['opi']
        self.goals = player_stats['goals']
        self.saves = player_stats['saves']
        self.score = player_stats['score']
        self.shots = player_stats['shots']
        self.assists = player_stats['assists']
        self.goals_against = player_stats['goals_against']
        self.shots_against = player_stats['shots_against']

    async def __update_from_members__(self,
                                      sprocket_members: {}) -> None:
        if not sprocket_members:
            return
        member = next((x for x in sprocket_members if x['discord_id'] == self.discord_member.id.__str__()), None)
        if not member:
            return
        self.mle_name = member['name']
        self.member_id = member['member_id']
        self.mle_id = member['mle_id']
        self.mle_player_id = member['mle_player_id']

    async def post_quick_info(self, ctx: discord.ext.commands.Context):
        embed = discord.Embed(color=discord.Color.dark_red(), title=f'**{self.mle_name} Quick Info**',
                              description='Quick info gathered by sprocket public datasets.\n')
        embed.add_field(name='`Name`', value=self.discord_member.name, inline=True)
        embed.add_field(name='`Display Name`', value=self.discord_member.mention, inline=True)
        embed.add_field(name='`MLE Name`', value=self.mle_name, inline=True)
        embed.add_field(name='`MLE ID`', value=self.mle_id, inline=True)
        embed.add_field(name='`Sprocket ID`', value=self.sprocket_id, inline=True)
        embed.add_field(name='`Salary`', value=self.salary, inline=True)
        embed.add_field(name='Scrim Points', value=self.scrim_points, inline=True)
        embed.add_field(name='Eligible?', value=self.eligible, inline=True)
        embed.add_field(name='Role', value=self.role, inline=True)
        embed.add_field(name='dpi', value=self.dpi, inline=True)  # This is disabled until sprocket gives out better data(?)
        embed.add_field(name='opi', value=self.opi, inline=True)
        embed.add_field(name='goals', value=self.goals, inline=True)
        embed.add_field(name='saves', value=self.saves, inline=True)
        embed.add_field(name='score', value=self.score, inline=True)
        embed.add_field(name='shots', value=self.shots, inline=True)
        embed.add_field(name='assists', value=self.assists, inline=True)
        embed.add_field(name='goals_against', value=self.goals_against, inline=True)
        embed.add_field(name='shots_against', value=self.shots_against, inline=True)
        await ctx.send(embed=embed)

    async def update(self, sprocket_data: {}):
        if not sprocket_data:
            return
        await self.__update_from_members__(sprocket_data['sprocket_members'])
        await self.__update_from_sprocket_players__(sprocket_data['sprocket_players'])
        await self.__update_from_sprocket_player_stats__(sprocket_data['sprocket_player_stats'])
        return self


def get_member_by_id(guild: discord.Guild, member_id: int) -> discord.Member | None:
    return next((x for x in guild.members if x.id == member_id), None)


def get_member_by_name(guild: discord.Guild, member_name: str):
    return next((x for x in guild.members if x.name.lower() == member_name.lower()), None)


def get_members_by_role_name(guild: discord.Guild, role: str):
    return [x for x in guild.members for y in x.roles if y.name == role]


def get_members_by_role(guild: discord.Guild, role: discord.Role):
    return [member for member in guild.members if role in member.roles]


def has_role(member: discord.Member, roles: [discord.Role]) -> bool:
    return next((True for role in roles if role in member.roles), False)
