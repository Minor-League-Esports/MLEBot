""" Minor League E-Sports Bot Commands
# Author: irox_rl
# Purpose: General Functions and Commands
# Version 3.00.01
"""
from PyDiscoBot import channels
import discord
from discord.ext import commands
from PyDiscoBot import err
import member
import roles
import team

""" System Error Strings 
"""
ERR_NO_PERMS = 'You do not have sufficient permissions to perform this action. Please contact someone with higher permissions than yours.'


class MLECommands(commands.Cog):
    def __init__(self,
                 master_bot,
                 ):
        self.bot = master_bot

    @commands.command(name='buildmembers', description='Build members for bot')
    async def buildmembers(self, ctx: discord.ext.commands.Context):
        if ctx.channel is not discord.DMChannel:
            if self.bot.admin_commands_channel is None or ctx.channel is not self.bot.admin_commands_channel:
                return
        if not member.has_role(ctx.author,
                               roles.GENERAL_MGMT_ROLES):
            return await self.bot.send_notification(ctx, ERR_NO_PERMS, True)
        await err(self.bot.franchise.build(self.bot.guild.members))

    @commands.command(name='clearchannel', description='clear channel messages')
    async def clearchannel(self, ctx: discord.ext.commands.Context, count: int):
        if not member.has_role(ctx.author,
                               roles.GENERAL_MGMT_ROLES):
            return await self.bot.send_notification(ctx, ERR_NO_PERMS, True)
        await channels.clear_channel_messages(ctx.channel, count)

    @commands.command(name='lookup', description='lookup player by MLE name provided')
    async def lookup(self,
                     ctx: discord.ext.commands.Context,
                     *mle_name):
        if ctx.channel is not discord.DMChannel:
            if self.bot.admin_commands_channel is None or ctx.channel is not self.bot.admin_commands_channel:
                return
        if not member.has_role(ctx.author,
                               roles.CAPTAIN_ROLES):
            return await self.bot.send_notification(ctx, ERR_NO_PERMS, True)
        mle_player = next((x for x in self.bot.sprocket.data['stonks'] if x['Player Name'] == ' '.join(mle_name)), None)
        if not mle_player:
            await ctx.reply('mle player not found in sprocket data')
            return
        sprocket_player = next(
            (x for x in self.bot.sprocket.data['sprocket_players'] if x['name'] == mle_player['Player Name']), None)
        if not sprocket_player:
            await ctx.reply('sprocket player not found in sprocket data')
            return

        embed = discord.Embed(color=discord.Color.dark_red(), title=f'**{" ".join(mle_name)} Quick Info**',
                              description='Quick info gathered by MLE docs\n')
        embed.add_field(name='`MLE Name`', value=mle_player['Player Name'], inline=True)
        embed.add_field(name='`MLE ID`', value=mle_player['mleid'], inline=True)
        embed.add_field(name='`Sprocket ID`', value=sprocket_player['member_id'], inline=True)
        embed.add_field(name='`Salary`', value=mle_player['Salary'], inline=True)
        embed.add_field(name='Scrim Points', value=mle_player['Scrim Points'], inline=True)
        embed.add_field(name='Eligible?', value=mle_player['Eligible?'], inline=True)
        embed.add_field(name='Role', value=mle_player['Slot'], inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='quickinfo', description='Get quick information about yourself')
    async def quickinfo(self, ctx: discord.ext.commands.Context):
        if ctx.channel is not discord.DMChannel:
            if self.bot.public_commands_channel is None or ctx.channel is not self.bot.public_commands_channel:
                if self.bot.admin_commands_channel is None or ctx.channel is not self.bot.admin_commands_channel:
                    return
        await self.bot.franchise.post_player_quick_info(ctx.author,
                                                        ctx)

    @commands.command(name='runroster',
                      description='Run a refresh of the roster channel')
    async def runroster(self, ctx: discord.ext.commands.Context):
        if ctx.channel is not discord.DMChannel:
            if self.bot.admin_commands_channel is None or ctx.channel is not self.bot.admin_commands_channel:
                return
        if not member.has_role(ctx.author,
                               roles.GENERAL_MGMT_ROLES):
            return await self.bot.send_notification(ctx, ERR_NO_PERMS, True)
        if await self.bot.roster.post_roster():
            await err('Roster posted successfully!')

    @commands.command(name='seasonstats',
                      description='get season stats for a specific league')
    async def seasonstats(self,
                          ctx: discord.ext.commands.Context,
                          league: str):
        if not league:
            return await self.bot.send_notification(ctx, 'You must specify a league when running this command.\n'
                                                         'i.e.: ub.seasonstats master', True)

        await self.bot.franchise.post_season_stats_html(league.lower(),
                                                        ctx)

    @commands.command(name='showmembers', description='Show all league members')
    async def showmembers(self, ctx: discord.ext.commands.Context):
        if ctx.channel is not discord.DMChannel:
            if self.bot.public_commands_channel is None or ctx.channel is not self.bot.public_commands_channel:
                if self.bot.admin_commands_channel is None or ctx.channel is not self.bot.admin_commands_channel:
                    return
        for _team in self.bot.franchise.teams:
            await self.desc_builder(ctx,
                                    team.get_league_text(_team.league),
                                    _team.players)

    @commands.command(name='updatesprocket',
                      description='Update internal information by probing sprocket for new sprocket_data')
    async def updatesprocket(self, ctx: discord.ext.commands.Context):
        if ctx.channel is not discord.DMChannel:
            if self.bot.admin_commands_channel is None or ctx.channel is not self.bot.admin_commands_channel:
                return
        if not member.has_role(ctx.author,
                               roles.GENERAL_MGMT_ROLES):
            return await self.bot.send_notification(ctx, ERR_NO_PERMS, True)
        self.bot.sprocket.reset()
        await self.bot.sprocket.run()
        await self.bot.send_notification(self.bot.notification_channel, 'League-Sprocket update complete.')

    async def desc_builder(self,
                           ctx: discord.ext.commands.Context,
                           title: str,
                           players: [member.Member]):
        for _p in players:
            await _p.__build_from_sprocket__(self.bot.sprocket.data)
        embed: discord.Embed = self.bot.default_embed(title, '')
        embed.add_field(name='name                                 sal       id',
                        value='\n'.join(
                            [f'` {_p.mle_name.ljust(16) if _p.mle_name else "N/A?".ljust(16)} {str(_p.salary).ljust(4) if _p.salary else "N/A?"} {str(_p.mle_id).ljust(4) if _p.mle_id else "N/A??   "} `'
                             for _p in players]),
                        inline=False)
        if self.bot.server_icon:
            embed.set_thumbnail(url=self.bot.get_emoji(self.bot.server_icon).url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if len(before.roles) != len(after.roles):
            for role in after.roles:
                if role.name == self.bot.franchise.franchise_name:
                    self.bot.roster.run_req = True
