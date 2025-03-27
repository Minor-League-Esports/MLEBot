#!/usr/bin/env python
""" Minor League E-Sports Bot Commands
# Author: irox_rl
# Purpose: General Functions and Commands
# Version 1.0.7
#
# v1.0.6 - revival after some sprocket updates and life getting in the way...
# v1.0.6 - Include slash commands
"""
from PyDiscoBot import channels
from PyDiscoBot import Pagination, InteractionPagination
from PyDiscoBot import ReportableError
from .embed_frames.salary_card import salary_card
from .embed_frames.usage_card import usage_card
from .enums import *
from .team import get_league_text
from .franchise import SALARY_CAP_PL, SALARY_CAP_ML, SALARY_CAP_CL, SALARY_CAP_AL, SALARY_CAP_FL

# non-local imports #
import discord
from discord import app_commands
from discord.ext import commands
import os
import dotenv


class MLECommands(commands.Cog):
    def __init__(self,
                 master_bot):
        self.bot = master_bot

    @property
    def sprocket(self):
        return self.bot.sprocket

    @property
    def sprocket_data(self):
        return self.bot.sprocket.data

    async def __local_lookup__(self,
                               interaction: discord.Interaction,
                               name: str):
        member = self.sprocket.get_member_from_name_str(name, try_match=True)
        if not member:
            return await self.bot.send_notification(interaction,
                                                    f'mle member "{name}" not found in sprocket `Members` dataset')
        player = self.sprocket.get_player_from_member(member)
        if not player:
            return await self.bot.send_notification(interaction,
                                                    f'mle member "{name}" not found in sprocket `Players` dataset')

        franchise = self.sprocket.get_franchise_from_player(player)
        player_tracker = self.sprocket.get_playerTracker_from_member(member)

        embed = salary_card(member,
                            player,
                            franchise,
                            player_tracker)

        await interaction.response.send_message(embed=embed)

    @staticmethod
    def get_sprocket_player_team_info(sprocket_player) -> str | None:
        return f"`{sprocket_player['slot'].removeprefix('PLAYER')} | {sprocket_player['salary']} | {sprocket_player['name']}`"

    @app_commands.command(name='clearchannel',
                          description='Clear channel messages. Include amt of messages to delete.\n Max is 100. (e.g. ub.clearchannel 55)')
    @app_commands.default_permissions()
    async def clearchannel(self,
                           interaction: discord.Interaction,
                           message_count: int):
        await interaction.response.defer()
        await channels.clear_channel_messages(interaction.channel, message_count)

    @app_commands.command(name='lookup',
                          description='Lookup player by MLE name provided.\nTo lookup yourself, just type {ub.lookup}')
    @app_commands.describe(mle_name='MLE Name of player to look up.')
    @app_commands.default_permissions()
    async def lookup(self,
                     interaction: discord.Interaction,
                     mle_name: str):
        await self.__local_lookup__(interaction,
                                    mle_name)

    @app_commands.command(name='rebuild',
                          description='Rebuild bot meta data.')
    @app_commands.guilds(1043295434828947547)
    @app_commands.default_permissions()
    async def rebuild(self,
                      interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.bot.rebuild():
            await self.bot.send_notification(interaction,
                                             'Success!.',
                                             as_followup=True)
        else:
            await self.bot.send_notification(interaction,
                                             'An error has occured.',
                                             as_followup=True)

    @app_commands.command(name='query',
                          description='Lookup groups of players by provided filter.')
    @app_commands.describe(league_filter='[PL, ML, CL, AL, FL]')
    @app_commands.describe(query_filter='[FA, RFA, Waivers, Pend]')
    @app_commands.describe(sorting='[salary, current_scrim_points, name]')
    @app_commands.choices(league_filter=[
        app_commands.Choice(name='PL', value='pl'),
        app_commands.Choice(name='ML', value='ml'),
        app_commands.Choice(name='CL', value='cl'),
        app_commands.Choice(name='AL', value='al'),
        app_commands.Choice(name='FL', value='fl')
    ],
        query_filter=[
            app_commands.Choice(name='FA', value='fa'),
            app_commands.Choice(name='RFA', value='rfa'),
            app_commands.Choice(name='Waivers', value='waivers'),
            app_commands.Choice(name='Pend', value='pend')
    ],
        sorting=[
            app_commands.Choice(name='Salary', value='salary'),
            app_commands.Choice(name='Scrim Points',
                                value='current_scrim_points'),
            app_commands.Choice(name='Name', value='name')
    ])
    @app_commands.default_permissions()
    async def query(self,
                    interaction: discord.Interaction,
                    league_filter: app_commands.Choice[str],
                    query_filter: str,
                    sorting: str):
        _league_enum = get_league_enum_by_short_text(league_filter.value)
        if not _league_enum:
            return await self.bot.send_notification(interaction,
                                                    'League not found. Please enter a valid league.)',
                                                    True)

        valid_queries = ['fa', 'waivers', 'rfa', 'pend']
        valid_sorts = ['salary', 'current_scrim_points', 'name']
        if query_filter.lower() not in valid_queries:
            return await self.bot.send_notification(interaction,
                                                    f'`{query_filter}` is an invalid query. Please try again.',
                                                    True)

        if sorting.lower() not in valid_sorts:
            return await self.bot.send_notification(interaction,
                                                    f'`{sorting}` is an invalid sorting type. Please try again.')

        data = self.bot.sprocket.data
        _players = sorted([x for x in data['sprocket_players'] if
                           x['franchise'].lower() == query_filter.lower() and x[
                               'skill_group'] == _league_enum.name.replace(
                               '_', ' ')], key=lambda x: x[sorting], reverse=True)

        if len(_players) == 0:
            emb: discord.Embed = self.bot.default_embed('**Filtered Players**\n\n',
                                                        'There were no players to be found for this query!')
            emb.set_thumbnail(url=self.bot.mle_logo_url)
            await interaction.followup.send(embed=emb)
            return

        async def get_page(page: int,
                           as_timout: bool = False):
            emb: discord.Embed = self.bot.default_embed(f'**Filtered Players**\n\n',
                                                        f'Players filtered for `{query_filter}`\n'
                                                        f'Sorted by `{sorting}`')
            emb.set_thumbnail(url=self.bot.mle_logo_url)
            if as_timout:
                emb.add_field(name=f'**`Timeout`**',
                              value='This command has timed out. Type `[ub.help]` for help.')
                emb.set_footer(text=f'Page 1 of 1')
                return emb, 0

            elements_per_page = 15
            offset = (page - 1) * elements_per_page
            emb.add_field(name=f'**Sal      | Points |    Name**',
                          value='\n'.join(
                              [
                                  f"`{_p['salary'].__str__().ljust(4)} | {_p['current_scrim_points'].__str__().ljust(4)} | {_p['name']}`"
                                  for _p in _players[offset:offset + elements_per_page]]),
                          inline=False)
            total_pages = Pagination.compute_total_pages(len(_players),
                                                         elements_per_page)

            emb.set_footer(text=f'Page {page} of {total_pages}')
            return emb, total_pages

        await InteractionPagination(interaction, get_page).navigate()

    @app_commands.command(name='regrosterchannel',
                          description='Register Franchise Roster Channel for roster posting functionality.')
    @app_commands.default_permissions()
    async def regrosterchannel(self,
                               interaction: discord.Interaction):
        _team = await self.__resolve_franchise__(interaction)
        if not _team:
            await self.bot.send_notification(interaction,
                                             'Could not resolve this franchise from sprocket data!',
                                             as_followup=False)
            return
        try:
            dotenv.set_key(dotenv.find_dotenv(),
                           f"{_team['name'].upper()}_ROSTER",
                           str(interaction.channel_id),
                           quote_mode='never')
            # os.environ[f"{_team['name'].upper()}_ROSTER"] = str(interaction.channel_id)
            await self.bot.send_notification(interaction,
                                             'Success!',
                                             as_followup=False)
        except KeyError:
            await self.bot.send_notification(interaction,
                                             'An error has occurred!',
                                             as_followup=False)

    @app_commands.command(name='runroster',
                          description='Run a refresh of the roster channel.')
    @app_commands.default_permissions()
    async def runroster(self,
                        interaction: discord.Interaction):
        await interaction.response.defer()
        _team = await self.__resolve_franchise__(interaction)
        if not _team:
            await self.bot.send_notification(interaction,
                                             'Could not resolve this franchise from sprocket data!',
                                             as_followup=True)
            return

        dotenv.load_dotenv()
        _channel_id = os.getenv(f"{_team['name'].upper()}_ROSTER")
        if not _channel_id:
            await self.bot.send_notification(interaction,
                                             'Roster channel has not been configured! Run /regrosterchannel!',
                                             as_followup=True)
            return

        _channel = next(
            (x for x in interaction.guild.channels if x.id.__str__() == str(_channel_id)), None)
        if not _channel:
            await self.bot.send_notification(interaction,
                                             'Roster channel has not been found! Run /regrosterchannel!',
                                             as_followup=True)
            return

        if await self.bot.roster.post_roster(_team,
                                             _channel):
            await self.bot.send_notification(interaction,
                                             'Success!',
                                             as_followup=True)
        else:
            await self.bot.send_notification(interaction,
                                             'Failure!',
                                             as_followup=True)

    @app_commands.command(name='salary',
                          description='Get salary and extra data about yourself from Sprocket.')
    @app_commands.default_permissions()
    async def salary(self,
                     interaction: discord.Interaction):
        member = self.bot.sprocket.get_member_from_interaction(interaction)
        await self.__local_lookup__(interaction, '' if member is None else member['name'])

    @commands.command(name='seasonstats',
                      description='Beta - Get season stats for a specific league.\n\tInclude league name. (e.g. ub.seasonstats master).\n\tNaming convention will be updated soon - Beta')
    @app_commands.default_permissions()
    async def seasonstats(self,
                          ctx: discord.ext.commands.Context,
                          league: str):
        return
        if not league:
            return await self.bot.send_notification(ctx, 'You must specify a league when running this command.\n'
                                                         'i.e.: ub.seasonstats master', True)

        await self.bot.franchise.post_season_stats_html(league.lower(),
                                                        ctx)

    @app_commands.command(name='showusage',
                          description='Show game usage stats for all league members of this franchise.')
    @app_commands.default_permissions()
    async def showusage(self,
                        interaction: discord.Interaction):
        await interaction.response.defer()
        franchise = self.bot.sprocket.get_franchise_from_interaction(
            interaction)
        if not franchise:
            return await self.bot.send_notification(interaction,
                                                    'Could not resolve this franchise from sprocket data!',
                                                    as_followup=True)

        players = self.bot.sprocket.get_players_from_franchise(franchise,
                                                               as_dict=True)
        if not players:
            return await self.bot.send_notification(interaction,
                                                    'Could not get players for this franchise from sprocket!',
                                                    as_followup=True)

        complex_players = {
            'players': players['players'],
            'PL': [{
                'player': x,
                'usage': self.bot.sprocket.get_role_usage_from_player(x),
            } for x in players['PL']] if players['PL'] else None,
            'ML': [{
                'player': x,
                'usage': self.bot.sprocket.get_role_usage_from_player(x),
            } for x in players['ML']] if players['ML'] else None,
            'CL': [{
                'player': x,
                'usage': self.bot.sprocket.get_role_usage_from_player(x),
            } for x in players['CL']] if players['CL'] else None,
            'AL': [{
                'player': x,
                'usage': self.bot.sprocket.get_role_usage_from_player(x),
            } for x in players['AL']] if players['AL'] else None,
            'FL': [{
                'player': x,
                'usage': self.bot.sprocket.get_role_usage_from_player(x),
            } for x in players['FL']] if players['FL'] else None,
        }

        embed = usage_card.usage_card(franchise,
                                      complex_players)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='teameligibility',
                          description='Show team eligibility. Include league after command.\n\t(e.g. ub.teameligibility fl)')
    @app_commands.describe(league='[PL, ML, CL, AL, FL]')
    @app_commands.choices(league=[
        app_commands.Choice(name='PL', value='pl'),
        app_commands.Choice(name='ML', value='ml'),
        app_commands.Choice(name='CL', value='cl'),
        app_commands.Choice(name='AL', value='al'),
        app_commands.Choice(name='FL', value='fl')
    ])
    @app_commands.default_permissions()
    async def teameligibility(self,
                              interaction: discord.Interaction,
                              league: str):
        if not league:
            await self.bot.send_notification(interaction,
                                             'You must specify a league when running this command!')
            return
        _league_enum = get_league_enum_by_short_text(league)
        if not _league_enum:
            await self.bot.send_notification(interaction,
                                             'League not found. Please enter a valid league.')
            return
        _league_text = get_league_text(_league_enum)

        franchise = self.bot.sprocket.get_franchise_from_interaction(
            interaction)
        if not franchise:
            return await self.bot.send_notification(interaction,
                                                    'Could not resolve this franchise from sprocket data!',
                                                    as_followup=True)

        _players = [x for x in self.bot.sprocket.data['sprocket_players']
                    if x['franchise'] == franchise['Franchise']]
        if not _players:
            await self.bot.send_notification(interaction,
                                             'Could not get players for this franchise from sprocket!',
                                             as_followup=True)
            return

        _league_players = sorted([x for x in _players if x['skill_group'] == _league_text and x['slot'] != 'NONE'],
                                 key=lambda x: x['slot'])
        if not _league_players:
            await self.bot.send_notification(interaction,
                                             'An error has occurred.')
            return

        await interaction.response.defer()
        embed = self.bot.default_embed(
            f"{_league_text} {franchise['Franchise']} Eligibility Information",
            color=discord.Color.from_str(franchise['Primary Color']))
        embed.set_thumbnail(url=franchise['Photo URL'])

        ljust_limit = 8

        for _p in _league_players:
            embed.add_field(name=f"**{_p['name']}**",
                            value=f"`{'Role:'.ljust(ljust_limit)}` {_p['slot']}\n"
                                  f"`{'Salary:'.ljust(ljust_limit)}` {_p['salary']}\n"
                                  f"`{'Points:'.ljust(ljust_limit)}` {_p['current_scrim_points'].__str__()}\n"
                                  f"`{'Until:'.ljust(ljust_limit)}` {_p['Eligible Until'].__str__()}",
                            inline=True)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='teaminfo',
                          description='Get information about a team from the league!\n\tInclude team after command. (e.g. ub.teaminfo sabres)')
    @app_commands.describe(_team_name='MLE Team to get info about.')
    @app_commands.default_permissions()
    async def teaminfo(self,
                       interaction: discord.Interaction,
                       _team_name: str):

        if not _team_name:
            raise ReportableError(
                'You must provide a team when running this command!')

        _team = next(
            (x for x in self.bot.sprocket.data['sprocket_teams'] if x['Franchise'].lower(
            ) == _team_name.lower()),
            None)
        if not _team:
            raise ReportableError(
                f'Could not find team `{_team_name}` in sprocket data base!\nPlease try again!')

        embed = team.get_mle_franchise_embed(_team)

        await interaction.response.defer()
        _team_players = team.get_defined_team_players(_team,
                                                      self.bot.sprocket.data)
        if not _team_players:
            raise ReportableError('Could not find players for franchise!')

        embed.add_field(name='**Franchise Manager**',
                        value=f"`{_team_players['fm']['name']}`" if _team_players['fm'] else "",
                        inline=False)

        embed.add_field(name='**General Manager**',
                        value=f"\n".join(
                            [f"`{gm['name']}`" for gm in _team_players['gms']]),
                        inline=False)

        if len(_team_players['agms']) != 0:
            embed.add_field(name='**Assistant General Managers**',
                            value=f"\n".join(
                                [f"`{agm['name']}`" for agm in _team_players['agms']]),
                            inline=False)

        if len(_team_players['captains']) != 0:
            embed.add_field(name='**Captains**',
                            value=f"\n".join(
                                [f"`{x['name']}`" for x in _team_players['captains']]),
                            inline=False)

        if len(_team_players['pr_supports']) != 0:
            embed.add_field(name='**PR Supports**',
                            value=f"\n".join(
                                [f"`{x['name']}`" for x in _team_players['pr_supports']]),
                            inline=False)

        embed.add_field(
            name='**Roster**', value='**`[Top5/SalCap] [CanSign] League`**', inline=False)

        self.__team_info_league__(sorted(_team_players['pl_players'], key=lambda _p: _p['slot']),
                                  embed,
                                  'Premier',
                                  SALARY_CAP_PL)

        self.__team_info_league__(sorted(_team_players['ml_players'], key=lambda _p: _p['slot']),
                                  embed,
                                  'Master',
                                  SALARY_CAP_ML)

        self.__team_info_league__(sorted(_team_players['cl_players'], key=lambda _p: _p['slot']),
                                  embed,
                                  'Champion',
                                  SALARY_CAP_CL)

        self.__team_info_league__(sorted(_team_players['al_players'], key=lambda _p: _p['slot']),
                                  embed,
                                  'Academy',
                                  SALARY_CAP_AL)

        self.__team_info_league__(sorted(_team_players['fl_players'], key=lambda _p: _p['slot']),
                                  embed,
                                  'Foundation',
                                  SALARY_CAP_FL)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='updatesprocket',
                          description='Update internal information by probing sprocket for new data.')
    @app_commands.default_permissions()
    async def updatesprocket(self,
                             interaction: discord.Interaction):
        await interaction.response.defer()
        self.bot.sprocket.reset()
        await self.bot.sprocket.run()
        await self.bot.send_notification(interaction,
                                         'League-Sprocket update complete.',
                                         as_followup=True)

    def __team_info_league__(self,
                             players: [],
                             embed: discord.Embed,
                             league_name: str,
                             salary_cap: float):
        if not players:
            return

        players_strings = '\n'.join(
            [self.get_sprocket_player_team_info(player) for player in players if player is not None])

        embed.add_field(
            name=get_team_salary_string(players,
                                        league_name,
                                        salary_cap),
            value=players_strings,
            inline=False)


def get_players_salary_ceiling(top_sals: [{}]) -> float:
    sal_ceiling = 0.0
    range_length = 5 if len(top_sals) >= 5 else len(top_sals)
    for i in range(range_length):
        sal_ceiling += top_sals[i]['salary']
    return sal_ceiling


def get_team_salary_string(players: [],
                           league_name: str,
                           salary_cap: float) -> str:
    top_sals = sorted(players,
                      key=lambda p: p['salary'],
                      reverse=True)
    sal_ceiling = get_players_salary_ceiling(top_sals)
    _sign = '+' if sal_ceiling >= salary_cap else '-'
    _signable_str = f"+{top_sals[-1]['salary'] + (salary_cap - sal_ceiling)}" if sal_ceiling <= salary_cap else "NONE"
    return f'**`[{sal_ceiling} / {salary_cap}] [{_signable_str}]` {league_name}**'


def get_league_enum_by_short_text(league: str):
    if not league:
        return None
    if league.lower() == 'pl':
        _league_enum = LeagueEnum.PREMIER_LEAGUE
    elif league.lower() == 'ml':
        _league_enum = LeagueEnum.MASTER_LEAGUE
    elif league.lower() == 'cl':
        _league_enum = LeagueEnum.CHAMPION_LEAGUE
    elif league.lower() == 'al':
        _league_enum = LeagueEnum.Academy_League
    elif league.lower() == 'fl':
        _league_enum = LeagueEnum.FOUNDATION_LEAGUE
    else:
        _league_enum = None
    return _league_enum
