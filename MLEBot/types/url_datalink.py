import datetime
import json
import requests
from pydiscobot.services.log import logger
from ..services.const import URL_REQ_TIMEOUT


class UrlDataLink:
    """url data link to grab json data from remote server and store it
    """

    def __init__(self,
                 name: str,
                 url_link: str):
        self.logger = logger(__name__+name)
        self.logger.info('initializing link -> %s | url -> %s...', name, url_link)
        self._time: datetime.datetime | None = None
        self._data = None
        self._name = name
        self._url = url_link
        self._initialized: bool = False

    @property
    def data(self) -> any:
        """get stored data

        Returns:
            any: stored data
        """
        return self._data

    @property
    def json_link(self) -> str:
        """url link appended with .json for easy direct-to-file saving

        Returns:
            str: string of url appended with .json
        """
        return '.' + self._name + '.json'

    def compress(self) -> dict:
        """compress data to dict

        Returns:
            dict: dict describing this link
        """
        return {
            'data': self._data,
            'time': self._time.strftime("%d/%m/%Y, %H:%M:%S"),
        }

    def decompress(self, data: dict):
        """restore compressed data back to link

        Args:
            data (dict): data to restore into link
        """
        try:
            self._data = data['data']
            self._time = datetime.datetime.strptime(
                data['time'], "%d/%m/%Y, %H:%M:%S")
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            self.logger.warning('load failure...%s - %s', self._name, e)
            self._data = None
            self._time = None

    def fetch(self):
        """fetch data from url

        Raises:
            ValueError: URL Link is empty or corrupt.
        """
        if not self._url:
            raise ValueError('URL Link is empty, cannot fetch data')

        self.logger.info('fetching %s...', self._url)
        self._data = requests.get(self._url,
                                  timeout=URL_REQ_TIMEOUT).json()
        self._time = datetime.datetime.now()
        self.save()

    def init(self):
        """initialize
        """
        if self._initialized:
            return
        try:
            self.load()
        except (FileNotFoundError, EOFError):
            pass
        finally:
            self._initialized = True

    def save(self):
        """save data to artifacts dir
        """
        self.logger.info('saving %s...', self.json_link)
        with open(self.json_link, 'w', encoding='utf-8') as f:
            json.dump(self.compress(), f)

    def load(self):
        """load data from artifacts dir
        """
        self.logger.info('loading %s...', self.json_link)
        with open(self.json_link, 'r', encoding='utf-8') as f:
            self.decompress(json.load(f))
