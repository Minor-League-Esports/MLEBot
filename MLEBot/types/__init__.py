"""Minor League E-Sports Types (Classes)
    """

from .enums import LeagueEnum
from .franchise import Franchise, TeamRocketLeague, TeamTrackmania, MLEFranchiseTeam
from .member import Member
from .player import PlayerRL
from .sprocket_links import SprocketLinks
from .url_datalink import UrlDataLink

__version__ = '1.1.1'

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
