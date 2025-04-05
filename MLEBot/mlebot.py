"""Minor League E-Sports PyDiscoBot implimentation
    """

import os
import discord
from discord.ext import commands as disco_commands
from pydiscobot import Bot
from .services.cmds import Commands
from .services import const
from .tasks.sprocket import Sprocket


class MLEBot(Bot):
    """minor league esports bot

    Args:
        Bot (_type_): parent bot
    """

    def __init__(self,
                 command_prefix: str | None,
                 bot_intents: discord.Intents | None,
                 command_cogs: list[disco_commands.Cog]):
        command_cogs.extend(Commands)
        super().__init__(command_prefix=command_prefix,
                         bot_intents=bot_intents,
                         command_cogs=command_cogs)
        self._sprocket = Sprocket(self)
        self._tasker.append(self._sprocket)
        self._guild_ids: list[dict] = []

    @property
    def activity(self) -> discord.Activity:
        return discord.Activity(type=discord.ActivityType.listening, name='hot farts being generated in the atmosphere by alien lizard men.')

    @property
    def guild_ids(self) -> list[dict]:
        """all tracked MLE guilds

        Returns:
            list[dict]: all tracked MLE guilds
        """
        return self._guild_ids

    @property
    def sprocket(self) -> Sprocket | None:
        """get sprocket task

        Returns:
            Sprocket | None: Sprocket task or None
        """
        return self._sprocket

    async def _build_guilds(self):
        self._guild_ids.clear()
        for team in const.ALL_TEAMS:
            try:
                _id = os.getenv(team).upper()
                self._guild_ids.append({'team': team,
                                        'id': _id})
            except AttributeError:
                continue

    async def rebuild(self):
        """rebuild list of known MLE guilds
        """
        await self._build_guilds()

    async def on_ready(self,
                       suppress_task=False) -> None:
        """on bot ready

        Args:
            suppress_task (bool, optional): don't run periodic task. Defaults to False.
        """
        if self._admin_info.initialized:
            self.logger.warning('already initialized!')
            return
        await super().on_ready(suppress_task)
        await self._build_guilds()
        await self.change_presence(activity=self.activity)
