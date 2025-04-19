"""MLE Bot Logical Services
    """

from . import sprocket
from .sprocket import lookup_franchise, lookup_rl

__version__ = '1.1.1'

__all__ = (
    'sprocket',
    'lookup_franchise',
    'lookup_rl',
)
