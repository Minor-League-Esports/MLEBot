#!/usr/bin/env python
""" Sprocket Data Link
# Author: irox_rl
# Purpose: Individualized sprocket_data link object for sprocket database
# Version 1.0.2
"""
# non-local imports #
import asyncio
import datetime
import requests


class SprocketDataLink:
    def __init__(self, url_link: str):
        self.url_link = url_link
        self.last_time_updated: datetime.datetime | None = None
        self.json_data = None

    def compress(self):
        return {
            'json_data': self.json_data,
            'last_time_updated': self.last_time_updated,
        }

    def decompress(self, pickle_data):
        self.json_data = pickle_data['json_data']
        self.last_time_updated = pickle_data['last_time_updated']

    async def data(self):
        if not self.url_link:
            raise ValueError('URL Link is empty, cannot fetch sprocket_data')
        self.json_data = requests.get(f'{self.url_link}.json').json()
        self.last_time_updated = datetime.datetime.now()
        await asyncio.sleep(2)
