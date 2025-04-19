"""Minor League E-Sports Types (Classes)
    """

from .enums import LeagueEnum

from .sprocket import (
    Franchise,
    Member,
    PlayerRL,
    TeamRocketLeague,
    TeamTrackmania,
    MLEFranchiseTeam,
    SprocketLinks
)
from .url_datalink import UrlDataLink

__version__ = '1.1.4'

__all__ = (
    'Franchise',
    'TeamRocketLeague',
    'TeamTrackmania',
    'Member',
    'MLEFranchiseTeam',
    'PlayerRL',
    'LeagueEnum',
    'SprocketLinks',
    'UrlDataLink',
)
