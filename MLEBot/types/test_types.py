"""test types for MLE Bot
    """
from __future__ import annotations

import unittest
from .. import const
from ..types import UrlDataLink


class TestUrlDataLink(unittest.TestCase):
    """test class url datalink
    """

    def test_build(self):
        """test data link builds
        """
        link = UrlDataLink('unit-test-link',
                           const.SPR_DL_TEAMS,
                           const.SPR_HK_TEAMS)
        self.assertIsNotNone(link)
