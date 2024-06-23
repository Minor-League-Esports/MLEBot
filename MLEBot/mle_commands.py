#!/usr/bin/env python
""" Minor League E-Sports Bot Commands
# Author: irox_rl
# Purpose: General Functions and Commands
# Version 1.0.6
#
# v1.0.6 - Include slash commands
"""
import PyDiscoBot
from PyDiscoBot import channels
from PyDiscoBot import Pagination, InteractionPagination

# local imports #
from enums import *
from member import Member
import roles
from team import get_league_text
from franchise import SALARY_CAP_PL, SALARY_CAP_ML, SALARY_CAP_CL, SALARY_CAP_AL, SALARY_CAP_FL

# non-local imports #
import difflib
import discord
from discord import app_commands
from discord.ext import commands


class MLECommands(commands.Cog):
    def __init__(self,
                 master_bot):
        self.bot = master_bot

    async def __local_lookup__(self,
                               interaction: discord.Interaction,
                               mle_name: str = None):
        data = self.bot.sprocket.data  # easier to write, shorter code

        # Find player in Sprocket Members dataset
        if mle_name:
            _member = next((x for x in data['sprocket_members'] if x['name'] == mle_name), None)
            if not _member:
                matches = difflib.get_close_matches(mle_name, [x['name'] for x in data['sprocket_members']],
                                                    1)
                if matches:
                    await self.bot.send_notification(interaction,
                                                     f"Could not find `{mle_name}` in sprocket `Members` dataset. Did you mean `{matches[0]}`?")
                    return
        else:
            _member = next(
                (x for x in data['sprocket_members'] if x['discord_id'].__str__() == interaction.user.id.__str__()),
                None)
        if not _member:
            await self.bot.send_notification(interaction,
                                             'mle member not found in sprocket `Members` dataset')
            return

        # Find player in Sprocket Players dataset
        _player = next((x for x in data['sprocket_players'] if x['member_id'] == _member['member_id']), None)
        if not _player:
            await self.bot.send_notification(interaction,
                                             'mle member not found in sprocket `Players` dataset')
            return

        # more data
        _team = next((x for x in data['sprocket_teams'] if x['name'] == _player['franchise']), None)
        tracker_player = next((x for x in data['sprocket_trackers'] if x['mleid'] == _member['mle_id']), None)

        # embed
        embed = (discord.Embed(
            color=discord.Color.from_str(_team['primary_color']) if _team else self.bot.default_embed_color,
            title=f"**{_member['name']} Sprocket Info**",
            description='Data gathered by sprocket public data links.\n'
                        'See more at [sprocket links](https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html)\n')
                 .set_footer(text=f'Generated: {self.bot.last_time}'))
        embed.set_thumbnail(url=self.bot.mle_logo_url if not _team else _team['logo_img_link'])
        embed.add_field(name='MLE Name', value=f"`{_member['name']}`", inline=True)
        embed.add_field(name='MLE ID', value=f"`{_member['mle_id']}`", inline=True)
        embed.add_field(name='Salary', value=f"`{_player['salary']}`", inline=True)
        embed.add_field(name='League', value=f"`{_player['skill_group']}`", inline=True)
        embed.add_field(name='Scrim Points', value=f"`{_player['current_scrim_points']}`", inline=True)
        embed.add_field(name='Eligible?', value="`Yes`" if _player['current_scrim_points'] >= 30 else "`No`",
                        inline=True)
        embed.add_field(name='Franchise', value=f"`{_player['franchise']}`", inline=True)
        embed.add_field(name='Staff Position', value=f"`{_player['Franchise Staff Position']}`", inline=True)
        embed.add_field(name='Role', value=f"`{_player['slot']}`", inline=True)
        if tracker_player:
            embed.add_field(name='**Tracker Link**', value=tracker_player['tracker'], inline=False)
        await interaction.response.send_message(embed=embed)

    def bot_loaded(self) -> bool:
        return self.bot.loaded

    async def cog_check(self,
                        ctx: discord.ext.commands.Context):
        if not self.bot_loaded():
            raise PyDiscoBot.BotNotLoaded('Bot is not yet loaded. Please try again.')
        return True

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
            app_commands.Choice(name='Scrim Points', value='current_scrim_points'),
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
                               '_', ' ')], key=lambda x: x[sorting])

        if len(_players) == 0:
            emb: discord.Embed = self.bot.default_embed(f'**Filtered Players**\n\n',
                                                        f'There were no players to be found for this query!')
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

    @app_commands.command(name='runroster',
                          description='Run a refresh of the roster channel.')
    @app_commands.default_permissions()
    async def runroster(self,
                        interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.bot.roster.post_roster():
            await self.bot.send_notification(interaction,
                                             '`Successfully ran updated roster schedule.`',
                                             as_followup=True)
        else:
            await self.bot.send_notification(interaction,
                                             '`An Error Has Occurred.`',
                                             as_followup=True)

    @app_commands.command(name='salary',
                          description='Get salary and extra data about yourself from provided sprocket data.')
    @app_commands.default_permissions()
    async def salary(self,
                     interaction: discord.Interaction):
        await self.__local_lookup__(interaction)

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

    @app_commands.command(name='showmembers',
                          description='Show all league members for this franchise.')
    @app_commands.default_permissions()
    async def showmembers(self,
                          interaction: discord.Interaction):
        await interaction.response.defer()
        _franchise = next((x for x in self.bot.franchises if x.guild == interaction.guild), None)
        if not _franchise:
            await self.bot.send_notification(interaction,
                                             'Guild not managed by this bot! Cannot find appropriate members!')

        for _team in _franchise.teams:
            await self.desc_builder(interaction,
                                    get_league_text(_team.league),
                                    _team.players,
                                    _franchise)

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

        _franchise = next((x for x in self.bot.franchises if x.guild == interaction.guild), None)
        if not _franchise:
            await self.bot.send_notification(interaction,
                                             'Guild not managed by this bot! Cannot find appropriate members!')

        _players = await _franchise.get_team_eligibility(_league_enum)

        if not _players:
            await self.bot.send_notification(interaction,
                                             'An error has occurred.')
            return

        await interaction.response.defer()
        embed = self.bot.default_embed(
            f'{get_league_text(_league_enum)} {_franchise.franchise_name} Eligibility Information',
            color=discord.Color.from_str(_franchise.sprocket_team['primary_color']))
        embed.set_thumbnail(url=_franchise.sprocket_team['logo_img_link'])

        ljust_limit = 8

        for _p in [_x for _x in _players if _x.role != 'NONE']:
            embed.add_field(name=f"**{_p.mle_name}**",
                            value=f"`{'Role:'.ljust(ljust_limit)}` {_p.role}\n"
                                  f"`{'Salary:'.ljust(ljust_limit)}` {_p.salary}\n"
                                  f"`{'Points:'.ljust(ljust_limit)}` {_p.scrim_points.__str__()}\n"
                                  f"`{'Until:'.ljust(ljust_limit)}` ~TBD~",
                            inline=True)

        # embed.add_field(name=f'{"Role".ljust(12)}  {"name".ljust(30)} {"sal".ljust(14)} {"id".ljust(8)} {"scrim pts"}    {"eligible?"}',
        #                 value='\n'.join([f'**`{p.role.ljust(7)}`**  `{str(p.mle_name.ljust(14)) if p.mle_name else "N/A?".ljust(14)}` `{str(p.salary).ljust(6) if p.salary else "N/A?".ljust(6)}` `{p.mle_id.__str__().ljust(8) if p.mle_id else "N/A?".ljust(8)}` `{p.scrim_points.__str__().ljust(8)}` `{"Yes" if p.eligible else "No"}`' for p in _players]),
        #                 inline=False)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name='teaminfo',
                          description='Get information about a team from the league!\n\tInclude team after command. (e.g. ub.teaminfo sabres)')
    @app_commands.describe(team='MLE Team to get info about')
    @app_commands.default_permissions()
    async def teaminfo(self,
                       interaction: discord.Interaction,
                       team: str):
        if not team:
            await self.bot.send_notification(interaction,
                                             'You must provide a team when running this command!')
            return
        _team = next((x for x in self.bot.sprocket.data['sprocket_teams'] if x['name'].lower() == team.lower()), None)
        if not _team:
            await self.bot.send_notification(interaction,
                                             f'Could not find team {team} in sprocket data base!\nPlease try again!')
            return

        embed = (discord.Embed(color=discord.Color.from_str(_team['primary_color']),
                               title=f"{_team['name']} Roster")
                 .set_footer(text=f'Generated: {self.bot.last_time}'))
        embed.set_thumbnail(url=_team['logo_img_link'])

        _team_players = [x for x in self.bot.sprocket.data['sprocket_players'] if x['franchise'] == _team['name']]
        if not _team_players:
            await self.bot.send_notification(interaction,
                                             'Could not find players for franchise!')
            return

        await interaction.response.defer()
        _fm = next((x for x in _team_players if x['Franchise Staff Position'] == 'Franchise Manager'), None)
        _gm = next((x for x in _team_players if x['Franchise Staff Position'] == 'General Manager'), None)
        _agms = [x for x in _team_players if x['Franchise Staff Position'] == 'Assistant General Manager']
        _captains = [x for x in _team_players if x['Franchise Staff Position'] == 'Captain']
        _pr_supports = [x for x in _team_players if x['Franchise Staff Position'] == 'PR Support']

        _pl_players = [x for x in _team_players if x['skill_group'] == 'Premier League' and x['slot'] != 'NONE']
        _ml_players = [x for x in _team_players if x['skill_group'] == 'Master League' and x['slot'] != 'NONE']
        _cl_players = [x for x in _team_players if x['skill_group'] == 'Champion League' and x['slot'] != 'NONE']
        _al_players = [x for x in _team_players if x['skill_group'] == 'Academy League' and x['slot'] != 'NONE']
        _fl_players = [x for x in _team_players if x['skill_group'] == 'Foundation League' and x['slot'] != 'NONE']

        if _fm:
            embed.add_field(name='**Franchise Manager**',
                            value=f"`{_fm['name']}`" if _fm else "",
                            inline=False)

        if _gm:
            embed.add_field(name='**General Manager**',
                            value=f"`{_gm['name']}`" if _gm else "",
                            inline=False)

        if len(_agms) != 0:
            embed.add_field(name='**Assistant General Managers**',
                            value=f"\n".join([f"`{x['name']}`" for x in _agms]),
                            inline=False)

        if len(_captains) != 0:
            embed.add_field(name='**Captains**',
                            value=f"\n".join([f"`{x['name']}`" for x in _captains]),
                            inline=False)

        if len(_pr_supports) != 0:
            embed.add_field(name='**PR Supports**',
                            value=f"\n".join([f"`{x['name']}`" for x in _pr_supports]),
                            inline=False)

        MLECommands.__team_info_league__(sorted(_pl_players, key=lambda _p: _p['slot']),
                                         embed,
                                         'Premier',
                                         SALARY_CAP_PL)

        MLECommands.__team_info_league__(sorted(_ml_players, key=lambda _p: _p['slot']),
                                         embed,
                                         'Master',
                                         SALARY_CAP_ML)

        MLECommands.__team_info_league__(sorted(_cl_players, key=lambda _p: _p['slot']),
                                         embed,
                                         'Champion',
                                         SALARY_CAP_CL)

        MLECommands.__team_info_league__(sorted(_al_players, key=lambda _p: _p['slot']),
                                         embed,
                                         'Academy',
                                         SALARY_CAP_AL)

        MLECommands.__team_info_league__(sorted(_fl_players, key=lambda _p: _p['slot']),
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

    async def desc_builder(self,
                           interaction: discord.Interaction,
                           title: str,
                           players: [Member],
                           _franchise):
        embed: discord.Embed = self.bot.default_embed(title,
                                                      '',
                                                      color=discord.Color.from_str(
                                                          _franchise.sprocket_team['primary_color']))
        embed.add_field(name='name                                 sal       id',
                        value='\n'.join(
                            [
                                f'` {_p.mle_name.ljust(16) if _p.mle_name else "N/A?".ljust(16)} {str(_p.salary).ljust(4) if _p.salary else "N/A?"} {str(_p.mle_id).ljust(4) if _p.mle_id else "N/A??   "} `'
                                for _p in players]),
                        inline=False)
        embed.set_thumbnail(url=_franchise.sprocket_team['logo_img_link'])
        await interaction.followup.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self,
                               before: discord.Member,
                               after: discord.Member):
        return
        if len(before.roles) != len(after.roles):
            for role in after.roles:
                if role in roles.FRANCHISE_ROLES:
                    self.bot.roster.run_req = True

    @staticmethod
    def __team_info_league__(players: [],
                             embed: discord.Embed,
                             league_name: str,
                             salary_cap: float):
        if players:
            top_sals = sorted(players,
                              key=lambda p: p['salary'],
                              reverse=True)
            sal_ceiling = 0.0
            range_length = 5 if len(players) >= 5 else len(players)
            for i in range(range_length):
                sal_ceiling += top_sals[i]['salary']
            embed.add_field(name=f'**`[{sal_ceiling} / {salary_cap}]` {league_name}**',
                            value='\n'.join(
                                [f"`{_p['slot'].removeprefix('PLAYER')} | {_p['salary']} | {_p['name']}`" for _p in
                                 players if _p['slot'] != 'NONE']),
                            inline=False)


def get_league_enum_by_short_text(league: str):
    if not league:
        return None
    if league.lower() == 'pl':
        _league_enum = LeagueEnum.Premier_League
    elif league.lower() == 'ml':
        _league_enum = LeagueEnum.Master_League
    elif league.lower() == 'cl':
        _league_enum = LeagueEnum.Champion_League
    elif league.lower() == 'al':
        _league_enum = LeagueEnum.Academy_League
    elif league.lower() == 'fl':
        _league_enum = LeagueEnum.Foundation_League
    else:
        _league_enum = None
    return _league_enum
