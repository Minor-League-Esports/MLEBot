"""Minor League E-Sports Bot Commands
    """
from . import test_commands

from .lookup import Lookup
from .query import Query
from .rebuild import Rebuild
from .salary import Salary
from .showusage import ShowUsage
from .teameligibility import TeamEligibility
from .teaminfo import TeamInfo
from .updatesprocket import UpdateSprocket


Commands = [
    Lookup,
    Query,
    Rebuild,
    Salary,
    ShowUsage,
    TeamEligibility,
    TeamInfo,
    UpdateSprocket,
]


__version__ = '1.1.4'

__all__ = (
    'Commands',
    'test_commands',
)
