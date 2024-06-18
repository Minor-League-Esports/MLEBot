#!/usr/bin/env python
""" Minor League E-Sports Bot Commands
# Author: irox_rl
# Purpose: General Functions and Commands
# Version 1.0.6
#
# v1.0.6 - include salary caps, update formatting for teamlookup and teameligibility
#           add teaminfo command
"""
import PyDiscoBot
from PyDiscoBot import channels
from PyDiscoBot import Pagination

# local imports #
from MLEBot.enums import *
from MLEBot.member import Member, has_role
import MLEBot.roles
from MLEBot.team import get_league_text
from MLEBot.franchise import SALARY_CAP_PL, SALARY_CAP_ML, SALARY_CAP_CL, SALARY_CAP_AL, SALARY_CAP_FL

# non-local imports #
import difflib
import discord
from discord.ext import commands


def has_gm_roles():
    async def predicate(ctx: discord.ext.commands.Context):
        if not has_role(ctx.author,
                        MLEBot.roles.GENERAL_MGMT_ROLES):
            raise PyDiscoBot.InsufficientPrivilege("You do not have sufficient privileges.")
        return True

    return commands.check(predicate)


def has_captain_roles():
    async def predicate(ctx: discord.ext.commands.Context):
        if not has_role(ctx.author,
                        MLEBot.roles.CAPTAIN_ROLES + MLEBot.roles.GENERAL_MGMT_ROLES):
            raise PyDiscoBot.InsufficientPrivilege("You do not have sufficient privileges.")
        return True

    return commands.check(predicate)


def is_admin_channel():
    async def predicate(ctx: discord.ext.commands.Context):
        chnl = await ctx.cog.get_admin_cmds_channel()
        if ctx.channel is chnl:
            return True
        raise PyDiscoBot.IllegalChannel("This channel does not support that.")

    return commands.check(predicate)


def is_public_channel():
    async def predicate(ctx: discord.ext.commands.Context):
        admin_chnl = await ctx.cog.get_admin_cmds_channel()
        chnl = await ctx.cog.get_public_cmds_channel()
        if ctx.channel is chnl or ctx.channel is admin_chnl:
            return True
        raise PyDiscoBot.IllegalChannel("This channel does not support that.")

    return commands.check(predicate)


class MLECommands(commands.Cog):
    def __init__(self,
                 master_bot):
        self.bot = master_bot

    async def get_admin_cmds_channel(self):
        return self.bot.admin_commands_channel

    async def get_public_cmds_channel(self):
        return self.bot.public_commands_channel

    @commands.command(name='buildmembers',
                      description='Build MLE members for the local franchise.\nThis uses local roles, not sprocket.')
    @has_gm_roles()
    @is_admin_channel()
    async def buildmembers(self,
                           ctx: discord.ext.commands.Context):
        await self.bot.franchise.rebuild()
        await self.bot.send_notification(ctx,
                                         'Userbase has been successfully rebuilt!',
                                         True)

    @commands.command(name='clearchannel',
                      description='Clear channel messages. Include amt of messages to delete.\n Max is 100. (e.g. ub.clearchannel 55)')
    @has_gm_roles()
    async def clearchannel(self,
                           ctx: discord.ext.commands.Context,
                           message_count: int):
        await channels.clear_channel_messages(ctx.channel, message_count)

    @commands.command(name='lookup',
                      description='Lookup player by MLE name provided.\nThis is CASE-SENSITIVE! (e.g. ub.lookup irox)\nTo lookup yourself, just type {ub.lookup}')
    @has_captain_roles()
    @is_admin_channel()
    async def lookup(self,
                     ctx: discord.ext.commands.Context,
                     *mle_name):
        data = self.bot.sprocket.data  # easier to write, shorter code

        # Find player in Sprocket Members dataset
        if mle_name:
            _member = next((x for x in data['sprocket_members'] if x['name'] == ' '.join(mle_name)), None)
            if not _member:
                matches = difflib.get_close_matches(' '.join(mle_name), [x['name'] for x in data['sprocket_members']],
                                                    1)
                if matches:
                    return await ctx.reply(
                        f"Could not find `{' '.join(mle_name)}` in sprocket `Members` dataset. Did you mean `{matches[0]}`?")
        else:
            _member = next(
                (x for x in data['sprocket_members'] if x['discord_id'].__str__() == ctx.author.id.__str__()), None)
        if not _member:
            return await ctx.reply('mle member not found in sprocket `Members` dataset')

        # Find player in Sprocket Players dataset
        _player = next((x for x in data['sprocket_players'] if x['member_id'] == _member['member_id']), None)
        if not _player:
            return await ctx.reply('mle member not found in sprocket `Players` dataset')

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
        await ctx.send(embed=embed)

    @commands.command(name='query',
                      description='Lookup groups of players by provided filter.\n'
                                  '(e.g. ub.query ml Waivers)\n'
                                  'Current supported filters = [`FA`, `RFA`, `Waivers`]')
    @has_captain_roles()
    @is_admin_channel()
    async def query(self,
                    ctx: discord.ext.commands.Context,
                    league_filter: str,
                    query_filter: str):
        _league_enum = get_league_enum_by_short_text(league_filter)
        if not _league_enum:
            await self.bot.send_notification(ctx,
                                             'League not found. Please enter a valid league. (e.g. ub.query fl [query filter])',
                                             True)

        valid_queries = ['FA', 'Waivers', 'RFA']
        if query_filter not in valid_queries:
            await self.bot.send_notification(ctx,
                                             f'`{query_filter}` is an invalid query. Please try again.',
                                             True)

        data = self.bot.sprocket.data
        _players = [x for x in data['sprocket_players'] if x['franchise'] == query_filter and x['skill_group'] == _league_enum.name.replace('_', ' ')]

        if len(_players) == 0:
            emb: discord.Embed = self.bot.default_embed(f'**Filtered Players**\n\n',
                                                        f'There were no players to be found for this query!')
            emb.set_thumbnail(url=self.bot.mle_logo_url)
            await ctx.send(embed=emb)
            return

        async def get_page(page: int,
                           as_timout: bool = False):
            emb: discord.Embed = self.bot.default_embed(f'**Filtered Players**\n\n',
                                                        f'Players filtered for `{query_filter}`')
            emb.set_thumbnail(url=self.bot.mle_logo_url)
            if as_timout:
                emb.add_field(name=f'**`Timeout`**',
                              value='This command has timed out. Type `[ub.help]` for help.')
                emb.set_footer(text=f'Page 1 of 1')
                return emb, 0

            elements_per_page = 15
            offset = (page - 1) * elements_per_page
            emb.add_field(name=f'**MLE Players**',
                          value='\n'.join(
                              [f"`{_p['salary']} | {_p['name']}`" for _p in _players[offset:offset + elements_per_page]]),
                          inline=False)
            total_pages = Pagination.compute_total_pages(len(_players),
                                                         elements_per_page)

            emb.set_footer(text=f'Page {page} of {total_pages}')
            return emb, total_pages

        await Pagination(ctx, get_page).navigate()

    @commands.command(name='runroster',
                      description='Run a refresh of the roster channel.')
    @has_gm_roles()
    @is_admin_channel()
    async def runroster(self,
                        ctx: discord.ext.commands.Context):
        await self.bot.send_notification(ctx,
                                         'Working on it...',
                                         True)
        if await self.bot.roster.post_roster():
            await self.bot.send_notification(ctx,
                                             'Roster posted successfully!',
                                             True)

    @commands.command(name='salary',
                      description='Get salary and extra data about yourself from provided sprocket data.')
    @is_public_channel()
    async def salary(self,
                     ctx: discord.ext.commands.Context):
        await self.lookup(ctx)

    @commands.command(name='seasonstats',
                      description='Beta - Get season stats for a specific league.\n\tInclude league name. (e.g. ub.seasonstats master).\n\tNaming convention will be updated soon - Beta')
    @has_captain_roles()
    @is_admin_channel()
    async def seasonstats(self,
                          ctx: discord.ext.commands.Context,
                          league: str):
        if not league:
            return await self.bot.send_notification(ctx, 'You must specify a league when running this command.\n'
                                                         'i.e.: ub.seasonstats master', True)

        await self.bot.franchise.post_season_stats_html(league.lower(),
                                                        ctx)

    @commands.command(name='showmembers', description='Show all league members for this franchise.')
    @is_public_channel()
    async def showmembers(self,
                          ctx: discord.ext.commands.Context):
        for _team in self.bot.franchise.teams:
            await self.desc_builder(ctx,
                                    get_league_text(_team.league),
                                    _team.players)

    @commands.command(name='teameligibility',
                      description='Show team eligibility. Include league after command.\n\t(e.g. ub.teameligibility fl)')
    @has_captain_roles()
    @is_admin_channel()
    async def teameligibility(self,
                              ctx: discord.ext.commands.Context,
                              league: str):
        if not league:
            await ctx.reply('You must specify a league when running this command! (e.g. ub.teameligibility fl)')
            return
        _league_enum = get_league_enum_by_short_text(league)
        if not _league_enum:
            await ctx.reply('League not found. Please enter a valid league. (e.g. ub.teameligibility fl)')

        _players = await self.bot.franchise.get_team_eligibility(_league_enum)

        if not _players:
            await ctx.reply('An error has occurred.')

        embed = self.bot.default_embed(
            f'{MLEBot.team.get_league_text(_league_enum)} {self.bot.franchise.franchise_name} Eligibility Information')
        if self.bot.server_icon:
            embed.set_thumbnail(url=self.bot.get_emoji(self.bot.server_icon).url)

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

        await ctx.send(embed=embed)

    @commands.command(name='teaminfo',
                      description='Get information about a team from the league!\n\tInclude team after command. (e.g. ub.teaminfo sabres)')
    @is_public_channel()
    async def teaminfo(self,
                       ctx: discord.ext.commands.Context,
                       team: str):
        if not team:
            await ctx.reply('You must provide a team when running this command! (e.g. ub.teaminfo ->Sabres<-"')
            return
        _team = next((x for x in self.bot.sprocket.data['sprocket_teams'] if x['name'].lower() == team.lower()), None)
        if not _team:
            await ctx.reply(f'Could not find team {team} in sprocket data base!\nPlease try again!')
            return

        embed = (discord.Embed(color=discord.Color.from_str(_team['primary_color']),
                               title=f"{_team['name']} Roster")
                 .set_footer(text=f'Generated: {self.bot.last_time}'))
        embed.set_thumbnail(url=_team['logo_img_link'])

        _team_players = [x for x in self.bot.sprocket.data['sprocket_players'] if x['franchise'] == _team['name']]
        if not _team_players:
            await ctx.reply('Could not find players for franchise!')
            return

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

        await ctx.send(embed=embed)

    @commands.command(name='updatesprocket',
                      description='Update internal information by probing sprocket for new data.')
    @has_gm_roles()
    @is_admin_channel()
    async def updatesprocket(self, ctx: discord.ext.commands.Context):
        await self.bot.send_notification(ctx,
                                         'Working on it...',
                                         True)
        self.bot.sprocket.reset()
        await self.bot.sprocket.run()
        await self.bot.send_notification(ctx,
                                         'League-Sprocket update complete.',
                                         True)

    async def desc_builder(self,
                           ctx: discord.ext.commands.Context,
                           title: str,
                           players: [Member]):
        for _p in players:
            await _p.update(self.bot.sprocket.data)
        embed: discord.Embed = self.bot.default_embed(title, '')
        embed.add_field(name='name                                 sal       id',
                        value='\n'.join(
                            [
                                f'` {_p.mle_name.ljust(16) if _p.mle_name else "N/A?".ljust(16)} {str(_p.salary).ljust(4) if _p.salary else "N/A?"} {str(_p.mle_id).ljust(4) if _p.mle_id else "N/A??   "} `'
                                for _p in players]),
                        inline=False)
        if self.bot.server_icon:
            embed.set_thumbnail(url=self.bot.get_emoji(self.bot.server_icon).url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self,
                               before: discord.Member,
                               after: discord.Member):
        if len(before.roles) != len(after.roles):
            for role in after.roles:
                if role in MLEBot.roles.FRANCHISE_ROLES:
                    self.bot.roster.run_req = True

    @staticmethod
    def __team_info_league__(players: [],
                             embed: discord.Embed,
                             league_name: str,
                             salary_cap: float):
        if players:
            top_sals = sorted(players, key=lambda p: p['salary'])
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
