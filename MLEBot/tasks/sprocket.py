import datetime
import json
import threading
from pydiscobot.services.log import logger
from ..types import SprocketLinks, UrlDataLink


class Sprocket:
    """sprocket bot task"""

    def __init__(self, parent):
        self.parent = parent
        self.logger = logger(__name__)

        self._links = SprocketLinks()
        self._loaded = False

        self.on_updated: list[callable] = []

        self._last_time_ran: datetime.datetime | None = None
        self._next_run_time: datetime.datetime | None = None

    @property
    def links(self) -> SprocketLinks:
        """get all url data links for sprocket

        Returns:
            SprocketLinks: dataclass of sprocket url datalinks
        """
        return self._links

    @property
    def iterlinks(self) -> list[UrlDataLink]:
        """get iterable links

        Returns:
            tuple[SprocketLinks]: sprocket data links
        """
        items = self._links.links()
        return items

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

    def _calc_next_fetch_time(self) -> None:
        self.logger.info('calculating next run time...')
        def _calc(last_time_ran: datetime.datetime,
                  hour_to_compare: int) -> datetime.datetime | None:

            now = datetime.datetime.now()

            # if we never ran.... well, run i guess?
            if not last_time_ran:
                self.logger.info('must update now...')
                return now

            # if it's a new day, run it
            if last_time_ran.day != now.day:
                self.logger.info('must update now...')
                return now

            # if we've ran already at this point today, return None
            if last_time_ran.hour >= hour_to_compare:
                return None

            # if we've passed the hour to compare and haven't updated, update now
            if hour_to_compare <= now.hour:
                self.logger.info('must update now...')
                return now

            # calculate the time till the next update time
            if last_time_ran.hour < hour_to_compare:
                update_time = (now + datetime.timedelta(hours=hour_to_compare - now.hour,
                                                        minutes=0 - now.minute,
                                                        seconds=0 - now.second))
                self.logger.info('set to update @ %s...', str(update_time))
                return update_time

        x = _calc(self._last_time_ran, 6)
        if x:
            self._next_run_time = x
            return

        x = _calc(self._last_time_ran, 12)
        if x:
            self._next_run_time = x
            return

        x = _calc(self._last_time_ran, 18)
        if x:
            self._next_run_time = x
            return

    async def _update(self):
        threads = [threading.Thread(name='fetch', target=link.fetch)
                   for link in self.iterlinks]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self._last_time_ran = datetime.datetime.now()

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
        self.load()

    async def run(self):
        """run this sprocket task
        """
        self.logger.info('running task...')
        if not self._loaded:
            self.init()
        if self.ready_to_update:
            self.logger.info('updating links...')
            await self._update()
        else:
            return
        self._calc_next_fetch_time()
        self.save()
        for callback in self.on_updated:
            await callback()
        await self.parent.notify('sprocket server links updated.')

    def save(self):
        """save run time data to artifacts file
        """
        self.logger.info('saving data to -> %s...', self.json_link)
        with open(self.json_link, 'w', encoding='utf-8') as f:
            json.dump({
                'last_time_ran': self._last_time_ran.strftime("%d/%m/%Y, %H:%M:%S"),
                'next_run_time': self._next_run_time.strftime("%d/%m/%Y, %H:%M:%S")
            }, f)
