"""Manage Sprocket data links for up-to-date information
    """
from __future__ import annotations


import datetime
import json
import threading


from pydiscobot import Task
from pydiscobot.types.err import BotNotLoaded


from ..types import SprocketLinks, UrlDataLink


class Sprocket(Task):
    """sprocket bot task"""

    def __init__(self, parent):
        super().__init__(parent)

        self._links = SprocketLinks()
        self._loaded = False
        self._updating = False

        self.on_updated: list[callable] = []

        self._last_time_ran: datetime.datetime | None = None
        self._next_run_time: datetime.datetime | None = None

        self.init()

    @property
    def links(self) -> SprocketLinks:
        """get all url data links for sprocket

        Returns:
            SprocketLinks: dataclass of sprocket url datalinks
        """
        if self.updating:
            raise BotNotLoaded('Sprocket links are updating!')
        return self._links

    @property
    def iterlinks(self) -> list[UrlDataLink]:
        """get iterable links

        Returns:
            tuple[SprocketLinks]: sprocket data links
        """
        return self.links.links()

    @property
    def ready_to_update(self) -> bool:
        """if sprocket has published, return True
        sprocket publishes on 6 Hr intervals
        starting @ 00:00

        Returns:
            bool: ready to update
        """
        return self._next_run_time <= datetime.datetime.now()

    @property
    def json_link(self) -> str:
        """url link appended with .json for easy direct-to-file saving

        Returns:
            str: string of url appended with .json
        """
        return '.' + self.__class__.__name__ + '.json'

    @property
    def updating(self) -> bool:
        """links are currently fetching data

        Returns:
            bool: updating
        """
        return self._updating

    def _calc_next_fetch_time(self) -> None:
        self.logger.info('calculating next run time...')

        def _generate(n: datetime.datetime,
                      hour: int):
            return n + (
                datetime.timedelta(days=0,
                                   hours=hour-n.hour,
                                   minutes=15-n.minute,
                                   seconds=0-n.second,
                                   microseconds=0-n.microsecond))

        now = datetime.datetime.now()
        if now.hour < 6:
            self._next_run_time = _generate(now, 6)

        elif now.hour < 12:
            self._next_run_time = _generate(now, 12)

        elif now.hour < 18:
            self._next_run_time = _generate(now, 18)

        else:
            self._next_run_time = _generate(now, 24)

        self.logger.info('next run time -> %s',
                         self._next_run_time.strftime("%m/%d/%Y, %H:%M:%S"))

    async def _update(self):
        threads = [threading.Thread(name='fetch', target=link.fetch)
                   for link in self.iterlinks]

        self._updating = True
        # any calls to our 'links' attr here
        # will raise an exception

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self._last_time_ran = datetime.datetime.now()

        self._links.compile_data()

        self._calc_next_fetch_time()

        self.save()

        self._updating = False

        for callback in self.on_updated:
            await callback()

        await self.parent.notify('sprocket server links updated.')

    def load(self):
        """load run times from artifacts file
        """
        try:
            self.logger.info('loading %s...', self.json_link)
            with open(self.json_link, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._last_time_ran = datetime.datetime.strptime(
                    data['last_time_ran'], "%d/%m/%Y, %H:%M:%S")
                self._next_run_time = datetime.datetime.strptime(
                    data['next_run_time'], "%d/%m/%Y, %H:%M:%S")
                self._loaded = True
        except (KeyError, FileNotFoundError, EOFError, json.JSONDecodeError, ValueError) as e:
            self.logger.info('file load error on -> %s...%s',
                             self.json_link, e)
            self._next_run_time = datetime.datetime.now()
            self._loaded = True

    def reset(self):
        """force run time request to now
        """
        self._next_run_time = datetime.datetime.now()

    def init(self):
        """initialize this sprocket task
        """
        self.logger.info('initializing task...')
        if self._loaded:
            self.logger.warning('already loaded!')
            return
        for link in self.iterlinks:
            link.init()
        self._links.compile_data()
        self.load()

    async def run(self):
        """run this sprocket task
        """
        if not self._loaded:
            self.init()
        if self.ready_to_update:
            self.logger.info('updating links...')
            await self._update()

    def save(self):
        """save run time data to artifacts file
        """
        self.logger.info('saving data to -> %s...', self.json_link)
        with open(self.json_link, 'w', encoding='utf-8') as f:
            json.dump({
                'last_time_ran': self._last_time_ran.strftime("%d/%m/%Y, %H:%M:%S"),
                'next_run_time': self._next_run_time.strftime("%d/%m/%Y, %H:%M:%S")
            }, f)
