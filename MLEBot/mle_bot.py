""" Minor League E-Sports Bot
# Author: irox_rl
# Purpose: General Functions of a League Franchise summarized in bot fashion!
# Version 1.1.0
#
# v1.0.6 - server integration
"""

from PyDiscoBot import Bot
from PyDiscoBot.commands import Commands

# local imports #
from franchise import Franchise
from mle_commands import MLECommands
from task_roster import Task_Roster
from task_sprocket import Task_Sprocket

# non-local imports #
import discord
from discord.ext import commands as disco_commands
import dotenv
import os


class MLEBot(Bot):
    mle_logo_url = "https://images-ext-1.discordapp.net/external/8g0PflayqZyQZe8dqTD_wYGPcCpucRWAsnIjV4amZhc/https/i.imgur.com/6anH1sI.png?format=webp&quality=lossless&width=619&height=619"

    def __init__(self,
                 command_prefix: str | None,
                 bot_intents: discord.Intents | None,
                 command_cogs: [disco_commands.Cog]):
        super().__init__(command_prefix=command_prefix,
                         bot_intents=bot_intents,
                         command_cogs=command_cogs)
        self._sprocket = Task_Sprocket(self)
        self._roster = Task_Roster(self)
        self._franchises: [Franchise] = []

    @property
    def franchises(self) -> [Franchise]:
        return self._franchises

    @property
    def loaded(self) -> bool:
        """ loaded status for bot\n
        override to include external processes that need to load when initiating
        """
        return super().loaded and self.sprocket.all_links_loaded and self.roster.loaded

    @property
    def roster(self) -> Task_Roster:
        return self._roster

    @property
    def sprocket(self) -> Task_Sprocket | None:
        return self._sprocket

    async def build_guilds(self):
        if not self.sprocket.all_links_loaded:
            self.sprocket.load()
        for team in self.sprocket.data['sprocket_teams']:
            _team_guild_id = os.getenv(team['name'].upper())
            if _team_guild_id != '':
                _team_guild = next((x for x in self.guilds if x.id == int(_team_guild_id)), None)
                if _team_guild:
                    _franchise = Franchise(self,
                                           _team_guild,
                                           team['name'])
                    self._franchises.append(_franchise)
                    await _franchise.init()

    async def get_help_cmds_by_user(self,
                                    ctx: discord.ext.commands.Context) -> [disco_commands.command]:
        user_cmds = [cmd for cmd in self.commands]
        for cmd in self.commands:
            for check in cmd.checks:
                try:
                    can_run = await check(ctx)
                    if not can_run:
                        user_cmds.remove(cmd)
                        break
                except disco_commands.CheckFailure:
                    user_cmds.remove(cmd)
                    break
                except AttributeError:  # in this instance, a predicate could not be checked. It does not exist (part of the base bot)
                    break
        return user_cmds

    async def on_ready(self,
                       suppress_task=False) -> None:
        """ Method that is called by discord when the bot connects to the supplied guild\n
        **param suppress_task**: if True, do NOT run periodic task at the end of this call\n
        **returns**: None\n
        """
        """ do not initialize more than once
        """
        if self._initialized:
            await self.change_presence(
                activity=discord.Activity(type=discord.ActivityType.playing, name='🐶 Bark Simulator 🐕'))
            return
        await super().on_ready(suppress_task)

        await self.sprocket.run()
        await self.build_guilds()

        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name='🐶 Bark Simulator 🐕'))

    async def on_task(self) -> None:
        await super().on_task()
        await self._sprocket.run()


if __name__ == '__main__':
    dotenv.load_dotenv()
    intents = discord.Intents(8)
    # noinspection PyDunderSlots
    intents.guilds = True
    # noinspection PyDunderSlots
    intents.members = True
    # noinspection PyDunderSlots
    intents.message_content = True
    # noinspection PyDunderSlots
    intents.messages = True
    bot = MLEBot(['ub.', 'Ub.', 'UB.'],
                 intents,
                 [Commands, MLECommands])
    bot.run(os.getenv('DISCORD_TOKEN'))
