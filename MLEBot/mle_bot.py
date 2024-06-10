""" Minor League E-Sports Bot
# Author: irox_rl
# Purpose: General Functions of a League Franchise summarized in bot fashion!
# Version 1.0.2
"""

from PyDiscoBot import Bot, channels, commands

# local imports #
from MLEBot.franchise import Franchise
from MLEBot.mle_commands import MLECommands
from MLEBot.roles import init as init_roles
from MLEBot.task_roster import Task_Roster
from MLEBot.task_sprocket import Task_Sprocket

# non-local imports #
import discord
from discord.ext import commands as disco_commands
import dotenv
import os


class MLEBot(Bot):
    def __init__(self,
                 command_prefix: str | None,
                 bot_intents: discord.Intents | None,
                 command_cogs: [disco_commands.Cog]):
        super().__init__(command_prefix=command_prefix,
                         bot_intents=bot_intents,
                         command_cogs=command_cogs)
        self._roster_channel: discord.TextChannel | None = None
        self._premier_channel: discord.TextChannel | None = None
        self._master_channel: discord.TextChannel | None = None
        self._champion_channel: discord.TextChannel | None = None
        self._academy_channel: discord.TextChannel | None = None
        self._foundation_channel: discord.TextChannel | None = None
        self._sprocket = Task_Sprocket(self)
        self._roster = Task_Roster(self)
        self._franchise = Franchise(self,
                                    self._guild,
                                    disable_premier_league=True if (os.getenv('PREMIER_CHANNEL') == '') else False,
                                    disable_foundation_league=True if (
                                                os.getenv('FOUNDATION_CHANNEL') == '') else False)

    @property
    def academy_channel(self) -> discord.TextChannel | None:
        """ return the academy channel
        """
        return self._academy_channel

    @property
    def champion_channel(self) -> discord.TextChannel | None:
        """ return the champion channel
                """
        return self._champion_channel

    @property
    def foundation_channel(self) -> discord.TextChannel | None:
        """ return the foundation channel
                        """
        return self._foundation_channel

    @property
    def franchise(self) -> Franchise:
        return self._franchise

    @property
    def master_channel(self) -> discord.TextChannel | None:
        """ return the master channel
                                """
        return self._master_channel

    @property
    def premier_channel(self) -> discord.TextChannel | None:
        """ return the premier channel
                                """
        return self._premier_channel

    @property
    def roster(self) -> Task_Roster:
        return self._roster

    @property
    def roster_channel(self) -> discord.TextChannel | None:
        """ return the roster channel
        """
        return self._roster_channel

    @property
    def sprocket(self) -> Task_Sprocket | None:
        return self._sprocket

    async def on_ready(self,
                       suppress_task=False) -> None:
        """ Method that is called by discord when the bot connects to the supplied guild\n
        **param suppress_task**: if True, do NOT run periodic task at the end of this call\n
        **returns**: None\n
        """
        """ do not initialize more than once
        """
        if self._initialized:
            return
        await super().on_ready(suppress_task)
        init_roles(self._guild)

        try:
            roster_channel_token: str | None = os.getenv('ROSTER_CHANNEL')
        except KeyError:
            roster_channel_token = None
        try:
            premier_channel_token: str | None = os.getenv('PREMIER_CHANNEL')
        except KeyError:
            premier_channel_token: str | None = None
        try:
            master_channel_token: str | None = os.getenv('MASTER_CHANNEL')
        except KeyError:
            master_channel_token = None
        try:
            champion_channel_token: str | None = os.getenv('CHAMPION_CHANNEL')
        except KeyError:
            champion_channel_token = None
        try:
            academy_channel_token: str | None = os.getenv('ACADEMY_CHANNEL')
        except KeyError:
            academy_channel_token = None
        try:
            foundation_channel_token: str | None = os.getenv('FOUNDATION_CHANNEL')
        except KeyError:
            foundation_channel_token: str | None = None

        self._roster_channel = channels.get_channel_by_id(roster_channel_token,
                                                          self._guild) if roster_channel_token else None

        self._premier_channel = channels.get_channel_by_id(premier_channel_token,
                                                           self._guild) if premier_channel_token else None

        self._master_channel = channels.get_channel_by_id(master_channel_token,
                                                          self._guild) if master_channel_token else None

        self._champion_channel = channels.get_channel_by_id(champion_channel_token,
                                                            self._guild) if champion_channel_token else None

        self._academy_channel = channels.get_channel_by_id(academy_channel_token,
                                                           self._guild) if academy_channel_token else None

        self._foundation_channel = channels.get_channel_by_id(foundation_channel_token,
                                                              self._guild) if foundation_channel_token else None

        await self.franchise.init(self._guild)

    async def on_task(self) -> None:
        await super().on_task()
        await self._sprocket.run()
        await self._roster.run()


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

    bot = MLEBot('ub.',
                 intents,
                 [commands.Commands, MLECommands])

    bot.run(os.getenv('DISCORD_TOKEN'))
