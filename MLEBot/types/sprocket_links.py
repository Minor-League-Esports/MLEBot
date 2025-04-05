"""sprocket data links
    """

from ..services import const
from ..types.url_datalink import UrlDataLink


class SprocketLinks:
    """sprocket data links
    """
    def __init__(self):
        self.members: UrlDataLink = UrlDataLink('members', const.SPR_DL_MEMBERS)
        self.players: UrlDataLink = UrlDataLink('players', const.SPR_DL_PLAYERS)
        self.player_stats: UrlDataLink = UrlDataLink('player_stats', const.SPR_DL_PLA_STATS)
        self.scrims: UrlDataLink = UrlDataLink('scrims', const.SPR_DL_SCRIMS)
        self.teams: UrlDataLink = UrlDataLink('teams', const.SPR_DL_TEAMS)
        self.fixtures: UrlDataLink = UrlDataLink('fixtures', const.SPR_DL_FIXT)
        self.match_grps: UrlDataLink = UrlDataLink('match_groups', const.SPR_DL_MAT_GRP)
        self.matches: UrlDataLink = UrlDataLink('matches', const.SPR_DL_MATCHES)
        self.trackers: UrlDataLink = UrlDataLink('trackers', const.SPR_DL_TRACKER)
        self.usages: UrlDataLink = UrlDataLink('usages', const.SPR_DL_USAGE)

    def links(self):
        """get iterable links from this sprocket links class
        """
        return [getattr(self, x) for x in dir(self) if isinstance(getattr(self, x), UrlDataLink)]
