"""Minor League E-Sports Bot Commands
    """

from .lo import Commands as lo_commands
from .mle import Commands as mle_commands
from .rl import Commands as rl_commands


Commands = lo_commands + mle_commands + rl_commands


__version__ = '1.1.3'

__all__ = (
    'Commands',
)
