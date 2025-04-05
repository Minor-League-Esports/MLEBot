"""embed frames for MLEBot
    """

from .card import mle_card
from .salary_card import salary_card
from .teameligibility_card import teameligibility_card
from .teaminfo_card import teaminfo_card
from .usage_card import usage_card

__version__ = "1.1.2"

__all__ = (
    "mle_card",
    "salary_card",
    'teameligibility_card',
    'teaminfo_card',
    "usage_card",
)
