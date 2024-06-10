#!/usr/bin/env python
""" Minor League E-Sports Enumerations
# Author: irox_rl
# Purpose: Host MLE related enumerations to be used throughout this project
# Version 1.0.2
"""

# local imports #

# non-local imports #
from enum import Enum


class LeagueEnum(Enum):
    """ MLE League Enumeration Class
    """
    Premier_League = 1
    Master_League = 2
    Champion_League = 3
    Academy_League = 4
    Foundation_League = 5
