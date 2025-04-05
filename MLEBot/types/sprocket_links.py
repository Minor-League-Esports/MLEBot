"""sprocket data links
    """

from ..services import const
from . import franchise
from .url_datalink import UrlDataLink


class SprocketLinks:
    """sprocket data links
    """

    def __init__(self):
        self.members: UrlDataLink = UrlDataLink('members', const.SPR_DL_MEMBERS, const.SPR_HK_MEMBERS,
                                                const.SPR_HK_MEMBERS_SECONDARY)
        self.players: UrlDataLink = UrlDataLink(
            'players', const.SPR_DL_PLAYERS, const.SPR_HK_PLAYERS)
        self.player_stats: UrlDataLink = UrlDataLink(
            'player_stats', const.SPR_DL_PLA_STATS, const.SPR_HK_PLA_STATS)
        self.scrims: UrlDataLink = UrlDataLink(
            'scrims', const.SPR_DL_SCRIMS, const.SPR_HK_SCRIMS)
        self.teams: UrlDataLink = UrlDataLink(
            'teams', const.SPR_DL_TEAMS, const.SPR_HK_TEAMS)
        self.fixtures: UrlDataLink = UrlDataLink(
            'fixtures', const.SPR_DL_FIXT, const.SPR_HK_FIXT)
        self.match_grps: UrlDataLink = UrlDataLink(
            'match_groups', const.SPR_DL_MAT_GRP, const.SPR_HK_MAT_GRP)
        self.matches: UrlDataLink = UrlDataLink(
            'matches', const.SPR_DL_MATCHES, const.SPR_HK_MATCHES)
        self.trackers: UrlDataLink = UrlDataLink(
            'trackers', const.SPR_DL_TRACKER, const.SPR_HK_TRACKER)
        self.usages: UrlDataLink = UrlDataLink(
            'usages', const.SPR_DL_USAGE, const.SPR_HK_USAGE)

        self._franchises: dict = {}

    def compile_data(self) -> None:
        """compile data (usually directly after updating all links)
        """
        if not self.teams.data:
            return

        for f in self.teams.data:
            self._franchises[f['Franchise'].lower()] = franchise.Franchise.from_sprocket_links(f,
                                                                                               self)

    def franchise(self,
                  name: str) -> franchise.Franchise | None:
        """get franchise by name

        Args:
            name (str): franchise name

        Returns:
            (Franchise | None): franchise or none
        """
        return self._franchises.get(name.lower(), None)

    def links(self):
        """get iterable links from this sprocket links class
        """
        return [getattr(self, x) for x in dir(self) if isinstance(getattr(self, x), UrlDataLink)]
