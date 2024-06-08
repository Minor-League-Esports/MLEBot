""" Periodic Task - Role
# Author: irox_rl
# Purpose: Manage roles of a franchise and roster channel information
# Version 3.00.01
"""
import channels
import datetime
import discord
import dotenv
from discord.ext import commands
import member
import os
import pickle
import roles
from typing import Callable

from err import err

dotenv.load_dotenv()
try:
    IMG_STAFF = os.getenv('IMG_STAFF')
except KeyError:
    IMG_STAFF = None

try:
    IMG_PREMIER = os.getenv('IMG_PREMIER')
except KeyError:
    IMG_PREMIER = None

try:
    IMG_MASTER = os.getenv('IMG_MASTER')
except KeyError:
    IMG_MASTER = None
try:
    IMG_CHAMPION = os.getenv('IMG_CHAMPION')
except KeyError:
    IMG_CHAMPION = None

try:
    IMG_ACADEMY = os.getenv('IMG_ACADEMY')
except KeyError:
    IMG_ACADEMY = None

try:
    IMG_FOUNDATION = os.getenv('IMG_FOUNDATION')
except KeyError:
    IMG_FOUNDATION = None


class Task_Roster:
    def __init__(self,
                 master_bot):
        self.bot = master_bot
        self.header_msg: discord.Message | None = None
        self.header_msg_id: str | None = None
        self.staff_msg: discord.Message | None = None
        self.staff_msg_id: str | None = None
        self.premier_msg: discord.Message | None = None
        self.premier_msg_id: str | None = None
        self.master_msg: discord.Message | None = None
        self.master_msg_id: str | None = None
        self.champion_msg: discord.Message | None = None
        self.champion_msg_id: str | None = None
        self.academy_msg: discord.Message | None = None
        self.academy_msg_id: str | None = None
        self.foundation_msg: discord.Message | None = None
        self.foundation_msg_id: str | None = None
        self.new_role_detected = False
        self.new_role_watchdog: bool = False
        self.watchdog_time: datetime.datetime | None = None
        self.run_req = False
        self.loaded = False
        self._file_name = 'roster_data.pickle'

    async def __role_update__(self):
        if not self.run_req:
            return
        self.run_req = False

        if not await self.__role_update_helper__(self.header_msg,
                                                 self.__get_header__):
            return

        if not await self.__role_update_helper__(self.staff_msg,
                                                 self.__get_staff__):
            return

        if not self.bot.franchise.premier_disabled:
            if not await self.__role_update_helper__(self.premier_msg,
                                                     self.__get_league__,
                                                     'Premier',
                                                     roles.premier):
                return

        if not await self.__role_update_helper__(self.master_msg,
                                                 self.__get_league__,
                                                 'Master',
                                                 roles.master):
            return

        if not await self.__role_update_helper__(self.champion_msg,
                                                 self.__get_league__,
                                                 'Champion',
                                                 roles.champion):
            return

        if not await self.__role_update_helper__(self.academy_msg,
                                                 self.__get_league__,
                                                 'Academy',
                                                 roles.academy):
            return

        if not self.bot.franchise.foundation_disabled:
            if not await self.__role_update_helper__(self.foundation_msg,
                                                     self.__get_league__,
                                                     'Foundation',
                                                     roles.foundation):
                return
        await err('Roster has been successfully updated!')

    async def __role_update_helper__(self,
                                     message: discord.Message,
                                     fun: Callable,
                                     *args) -> bool:
        if not message:
            self.run_req = False
            await self.post_roster()
            return False
        await message.edit(embed=fun(*args))
        return True

    def __get_header__(self) -> discord.Embed:
        embed = discord.Embed(color=discord.Color.dark_red(), title=f'**{self.bot.franchise.franchise_name} Roster**\n',
                              description=f"For help, type 'ub.help'\n"
                                          f"Hello! I'm the your Utility Bot!")
        embed.add_field(name='Version', value=self.bot.version, inline=True)
        embed.set_footer(text=f'Generated: {self.bot.time}')  # Set footer information with notify time
        return embed

    def __get_staff__(self) -> discord.Embed:
        embed = discord.Embed(color=discord.Color.dark_red(), title='**Franchise Staff**\n\n',
                              description="")
        embed.add_field(name='**Franchise Manager**',
                        value='\n'.join(
                            [f'{x.mention}' for x in
                             member.get_members_by_role(self.bot.guild, roles.franchise_manager)]),
                        inline=True)
        embed.add_field(name='**Rocket League General Manager**',
                        value='\n'.join(
                            [f'{x.mention}' for x in
                             member.get_members_by_role(self.bot.guild, roles.general_manager_rl)]),
                        inline=True)
        embed.add_field(name='**Trackmania General Managers**',
                        value='\n'.join(
                            [f'{x.mention}' for x in
                             member.get_members_by_role(self.bot.guild, roles.general_manager_tm)]),
                        inline=True)
        embed.add_field(name='**Rocket League Assistant General Managers**', value='\n'.join(
            [f'{x.mention}' for x in member.get_members_by_role(self.bot.guild, roles.assistant_general_manager_rl)]),
                        inline=False)
        embed.add_field(name='**Trackmania Assistant General Managers**', value='\n'.join(
            [f'{x.mention}' for x in member.get_members_by_role(self.bot.guild, roles.assistant_general_manager_tm)]),
                        inline=False)
        embed.add_field(name='**Captains**',
                        value='\n'.join(
                            [f'{x.mention}' for x in member.get_members_by_role(self.bot.guild, roles.captain)]),
                        inline=True)
        embed.add_field(name='**Social Media**',
                        value='\n'.join(
                            [f'{x.mention}' for x in
                             member.get_members_by_role(self.bot.guild, roles.social_media)]),
                        inline=False)
        return embed

    def __get_league__(self,
                       league: str,
                       role: discord.Role,
                       descr: str = '') -> discord.Embed:
        embed = discord.Embed(color=discord.Color.dark_red(), title=f'**{league} League**',
                              description=f'{descr}\n')
        embed.description += '\n'.join(self.__strobe_league_members__(member.get_members_by_role(self.bot.guild, role)))
        return embed

    @staticmethod
    def __strobe_league_members__(league_members) -> []:
        max_player_cnt = 7
        line = []
        player_count = 0
        for _member in league_members:
            line.append(f'- {_member.mention}')
            player_count += 1
        if player_count < max_player_cnt:
            for x in range(player_count, max_player_cnt):
                line.append(f'- ')
        return line

    async def load(self):
        if not self.bot.roster_channel:
            return
        self.loaded = True
        try:
            with (open(self._file_name, 'rb') as f):  # Open save file
                data = pickle.load(f)
                self.header_msg = await channels.get_channel_message_by_id(self.bot.roster_channel,
                                                                           data['header_msg_id'].__str__())
                self.staff_msg = await channels.get_channel_message_by_id(self.bot.roster_channel,
                                                                          data['staff_msg_id'].__str__())
                self.premier_msg = await channels.get_channel_message_by_id(self.bot.roster_channel,
                                                                            data[
                                                                                'premier_msg_id'].__str__()) if not self.bot.franchise.premier_disabled else None
                self.master_msg = await channels.get_channel_message_by_id(self.bot.roster_channel,
                                                                           data['master_msg_id'].__str__())
                self.champion_msg = await channels.get_channel_message_by_id(self.bot.roster_channel,
                                                                             data['champion_msg_id'].__str__())
                self.academy_msg = await channels.get_channel_message_by_id(self.bot.roster_channel,
                                                                            data['academy_msg_id'].__str__())
                self.foundation_msg = await channels.get_channel_message_by_id(self.bot.roster_channel,
                                                                               data[
                                                                                   'foundation_msg_id'].__str__()) if not self.bot.franchise.foundation_disabled else None
                if any([not self.header_msg,
                        not self.staff_msg,
                        (not self.premier_msg if not self.bot.franchise.premier_disabled else False),
                        not self.master_msg,
                        not self.champion_msg,
                        not self.academy_msg,
                        not self.foundation_msg if not self.bot.franchise.foundation_disabled else False]):
                    raise ValueError
                return
        except FileNotFoundError:
            print('no file found for roster data')
        except EOFError:
            print('file corrupt for roster sprocket_data')
        except KeyError:
            print('file sprocket_data not valid for roster sprocket_data')
        except ValueError:
            print('Not all messages found for roster channel')
        await self.post_roster()

    async def post_roster(self, ctx: discord.ext.commands.Context | discord.TextChannel | None = None) -> bool:
        if ctx:
            context = ctx
        else:
            context = self.bot.roster_channel
            success = await channels.clear_channel_messages(context, 100)
            if not success:
                await err('Could not delete messages from roster channel!\n'
                          'Please manually delete them and retry running the ub.runroster command again.')
                return False

        header_msg = await context.send(embed=self.__get_header__())
        await channels.post_image(context, IMG_STAFF) if IMG_STAFF else None
        staff_msg = await context.send(embed=self.__get_staff__())
        if self.bot.franchise.premier_league is not None:
            await channels.post_image(context, IMG_PREMIER) if IMG_PREMIER else None
            premier_msg = await context.send(embed=self.__get_league__('Premier', roles.premier))
        else:
            premier_msg = None
        await channels.post_image(context, IMG_MASTER) if IMG_MASTER else None
        master_msg = await context.send(embed=self.__get_league__('Master', roles.master))
        await channels.post_image(context, IMG_CHAMPION) if IMG_CHAMPION else None
        champion_msg = await context.send(embed=self.__get_league__('Champion', roles.champion))
        await channels.post_image(context, IMG_ACADEMY) if IMG_ACADEMY else None
        academy_msg = await context.send(embed=self.__get_league__('Academy', roles.academy))
        if self.bot.franchise.foundation_league is not None:
            await channels.post_image(context, IMG_FOUNDATION) if IMG_FOUNDATION else None
            foundation_msg = await context.send(embed=self.__get_league__('Foundation', roles.foundation))
        else:
            foundation_msg = None
        await err('Roster has been successfully been re-created!')
        if not ctx:
            self.header_msg = header_msg
            self.staff_msg = staff_msg
            self.premier_msg = premier_msg
            self.master_msg = master_msg
            self.champion_msg = champion_msg
            self.academy_msg = academy_msg
            self.foundation_msg = foundation_msg
            self.save()
        return True

    async def run(self):
        if not self.loaded:
            await self.load()
        await self.__role_update__()

    def save(self):
        with open(self._file_name, 'wb') as f:
            try:
                pickle.dump({
                    'header_msg_id': self.header_msg.id,
                    'staff_msg_id': self.staff_msg.id,
                    'premier_msg_id': self.premier_msg.id if self.premier_msg else None,
                    'master_msg_id': self.master_msg.id,
                    'champion_msg_id': self.champion_msg.id,
                    'academy_msg_id': self.academy_msg.id,
                    'foundation_msg_id': self.foundation_msg.id if self.foundation_msg else None,
                }, f)
            except AttributeError:
                print('could not save roster information')
