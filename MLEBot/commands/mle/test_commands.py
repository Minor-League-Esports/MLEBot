"""test commands for pydisco bot
    """
from __future__ import annotations


import unittest


from .lookup import Lookup


__all__ = (
    'TestCommands',
)


class TestCommands(unittest.TestCase):
    """test commands for pydisco bot
    """

    def test_lookup(self):
        """test lookup command
        """
        cmd = Lookup()
        self.assertIsNotNone(cmd)  # to update later
