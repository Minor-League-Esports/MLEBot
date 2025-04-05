"""url data link to grab json data from remote server and store it
    """

import json
from typing import Any
import requests
from pydiscobot.services.log import logger
from ..services.const import URL_REQ_TIMEOUT


class UrlDataLink:
    """url data link to grab json data from remote server and store it
    currently supports 2 hashes.
    could extend to any amount, but not currently needed, so i'll worry about that logic later
    """

    def __init__(self,
                 name: str,
                 url_link: str,
                 hash_key: str | None = None,
                 second_hash_key: str | None = None):
        self.logger = logger(__name__+name)
        self._data = None
        self._hash_data = None
        self._secondary_hash_data = None
        self._name = name
        self._url = url_link
        self._hash_key = hash_key
        self._secondary_hash_key = second_hash_key
        self._initialized: bool = False

    @property
    def data(self) -> any:
        """get stored data

        Returns:
            any: stored data
        """
        return self._data

    @data.setter
    def data(self, value: dict) -> None:
        """set stored data
        also, process hash info

        Args:
            value (dict): dictionary to store into data
        """
        self._process_data(value)

    @property
    def json_link(self) -> str:
        """url link appended with .json for easy direct-to-file saving

        Returns:
            str: string of url appended with .json
        """
        return '.' + self._name + '.json'

    def _clear(self) -> None:
        self._data = None
        self._hash_data = None
        self._secondary_hash_data = None

    def _process_data(self,
                      data: dict) -> None:
        """hash data for quick lookup
        """
        self._clear()

        self._data = data

        if not self._hash_key:
            return

        self._hash_data = {}
        for key in data:
            self._hash_data[key[self._hash_key]] = key

        if not self._secondary_hash_key:
            return

        self._secondary_hash_data = {}
        for key in data:
            self._secondary_hash_data[key[self._secondary_hash_key]] = key

    def compress(self) -> dict:
        """compress data to dict

        Returns:
            dict: dict describing this link
        """
        return {
            'data': self._data,
        }

    def decompress(self, data: dict):
        """restore compressed data back to link

        Args:
            data (dict): data to restore into link
        """
        try:
            self.data = data['data']
        except (json.decoder.JSONDecodeError, ValueError, KeyError) as e:
            self.logger.warning('load failure...%s - %s', self._name, e)
            self._clear()

    def fetch(self):
        """fetch data from url

        Raises:
            ValueError: URL Link is empty or corrupt.
        """
        if not self._url:
            raise ValueError('URL Link is empty, cannot fetch data')

        self.logger.info('fetching %s...', self._url)
        self.data = requests.get(self._url,
                                 timeout=URL_REQ_TIMEOUT).json()
        self.save()

    def from_hash(self,
                  key: str) -> Any:
        """get data from hash storage, or none if not stored

        Args:
            key (str): key value to lookup

        Raises:
            ValueError: no data for key was found (data[key] == NotFound)

        Returns:
            Any: data from hash table
        """
        if not self._hash_data:
            raise ValueError('no hash data to retrieve!')

        return self._hash_data.get(key, None)

    def from_secondary_hash(self,
                            key: str) -> Any:
        """get data from hash storage, or none if not stored

        Args:
            key (str): key value to lookup

        Raises:
            ValueError: no data for key was found (data[key] == NotFound)

        Returns:
            Any: data from hash table
        """
        if not self._secondary_hash_data:
            raise ValueError('no hash data to retrieve!')

        return self._secondary_hash_data.get(key, None)

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
            try:
                self.decompress(json.load(f))
            except json.decoder.JSONDecodeError as e:
                self.logger.warning('failed to load file -> %s', e)
