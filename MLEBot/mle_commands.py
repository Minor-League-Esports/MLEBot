#!/usr/bin/env python
""" Minor League E-Sports Bot Commands
# Author: irox_rl
# Purpose: General Functions and Commands
# Version 1.0.4
"""
import PyDiscoBot
from PyDiscoBot import channels, err

# local imports #
from MLEBot.enums import *
from MLEBot.member import Member, has_role
import MLEBot.roles
from MLEBot.team import get_league_text

# non-local imports #
import discord
from discord.ext import commands

""" System Error Strings 
"""
ERR_NO_PERMS = 'You do not have sufficient permissions to perform this action. Please contact someone with higher permissions than yours.'


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
                 master_bot,
                 ):
        self.bot = master_bot

    async def get_admin_cmds_channel(self):
        return self.bot.admin_commands_channel

    async def get_public_cmds_channel(self):
        return self.bot.public_commands_channel

    @commands.command(name='buildmembers', description='Build MLE members for bot.')
    @has_gm_roles()
    @is_admin_channel()
    async def buildmembers(self, ctx: discord.ext.commands.Context):
        await self.bot.franchise.rebuild()
        await ctx.reply('Userbase has been successfully rebuilt!')

    @commands.command(name='clearchannel', description='Clear channel messages. Include amt of messages to delete, max is 100. (e.g. ub.clearchannel 55)')
    @has_gm_roles()
    async def clearchannel(self, ctx: discord.ext.commands.Context, count: int):
        await channels.clear_channel_messages(ctx.channel, count)

    @commands.command(name='lookup', description='Lookup player by MLE name provided. This is CASE-SENSITIVE!\n(e.g. ub.lookup irox)')
    @has_captain_roles()
    @is_admin_channel()
    async def lookup(self,
                     ctx: discord.ext.commands.Context,
                     *mle_name):
        mle_player = next((x for x in self.bot.sprocket.data['sprocket_members'] if x['name'] == ' '.join(mle_name)), None)
        if not mle_player:
            await ctx.reply('mle player not found in sprocket data')
            return
        sprocket_player = next(
            (x for x in self.bot.sprocket.data['sprocket_players'] if x['member_id'] == mle_player['member_id']), None)
        if not sprocket_player:
            await ctx.reply('sprocket player not found in sprocket data')
            return

        embed = discord.Embed(color=self.bot.default_embed_color, title=f'**{" ".join(mle_name)} Quick Info**',
                              description='Quick info gathered by MLE docs\n')
        embed.add_field(name='`MLE Name`', value=mle_player['name'], inline=True)
        embed.add_field(name='`MLE ID`', value=mle_player['mle_id'], inline=True)
        embed.add_field(name='`Sprocket ID`', value=sprocket_player['sprocket_player_id'], inline=True)
        embed.add_field(name='`Salary`', value=sprocket_player['salary'], inline=True)
        embed.add_field(name='Scrim Points', value=sprocket_player['current_scrim_points'], inline=True)
        embed.add_field(name='Eligible?', value="Yes" if sprocket_player['current_scrim_points'] >= 30 else "No", inline=True)
        embed.add_field(name='Role', value=sprocket_player['slot'], inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='quickinfo', description='Get quick information about yourself.')
    @is_public_channel()
    async def quickinfo(self, ctx: discord.ext.commands.Context):
        await self.bot.franchise.post_player_quick_info(ctx.author, ctx)

    @commands.command(name='runroster',
                      description='Run a refresh of the roster channel.')
    @has_gm_roles()
    @is_admin_channel()
    async def runroster(self, ctx: discord.ext.commands.Context):
        if await self.bot.roster.post_roster():
            await ctx.reply('Roster posted successfully!')

    @commands.command(name='seasonstats',
                      description='Beta - Get season stats for a specific league. Include league name.\n(e.g. ub.seasonstats master). Naming convention will be updated soon - Beta')
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
    async def showmembers(self, ctx: discord.ext.commands.Context):
        for _team in self.bot.franchise.teams:
            await self.desc_builder(ctx,
                                    get_league_text(_team.league),
                                    _team.players)

    @commands.command(name='teameligibility', description='Show team eligibility. Include league after command.\n(e.g. ub.teameligibility fl)')
    @has_captain_roles()
    @is_admin_channel()
    async def teameligibility(self,
                              ctx: discord.ext.commands.Context,
                              league: str):
        if not league:
            await ctx.reply('You must specify a league when running this command! (e.g. ub.teameligibility fl)')
            return
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
        if not _league_enum:
            await ctx.reply('League not found. Please enter a valid league. (e.g. ub.teameligibility fl)')

        _players = await self.bot.franchise.get_team_eligibility(_league_enum)

        if not _players:
            await ctx.reply('An error has occurred.')

        embed = self.bot.default_embed(f'{MLEBot.team.get_league_text(_league_enum)} {self.bot.franchise.franchise_name} Eligibility Information')
        embed.add_field(name=f'{"Role".ljust(12)}  {"name".ljust(30)} {"sal".ljust(14)} {"id".ljust(8)} {"scrim pts"}    {"eligible?"}',
                        value='\n'.join([f'**`{p.role.ljust(7)}`**  `{str(p.mle_name.ljust(14)) if p.mle_name else "N/A?".ljust(14)}` `{str(p.salary).ljust(6) if p.salary else "N/A?".ljust(6)}` `{p.mle_id.__str__().ljust(8) if p.mle_id else "N/A?".ljust(8)}` `{p.scrim_points.__str__().ljust(8)}` `{"Yes" if p.eligible else "No"}`' for p in _players]),
                        inline=False)
        if self.bot.server_icon:
            embed.set_thumbnail(url=self.bot.get_emoji(self.bot.server_icon).url)
        await ctx.send(embed=embed)


    @commands.command(name='updatesprocket',
                      description='Update internal information by probing sprocket for new data.')
    @has_gm_roles()
    @is_admin_channel()
    async def updatesprocket(self, ctx: discord.ext.commands.Context):
        await ctx.reply('Working on it...')
        self.bot.sprocket.reset()
        await self.bot.sprocket.run()
        await ctx.reply('League-Sprocket update complete.')

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
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if len(before.roles) != len(after.roles):
            for role in after.roles:
                if role in MLEBot.roles.FRANCHISE_ROLES:
                    self.bot.roster.run_req = True
