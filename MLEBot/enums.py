#!/usr/bin/env python
""" Minor League E-Sports Enumerations
# Author: irox_rl
# Purpose: Host MLE related enumerations to be used throughout this project
# Version 1.0.3
#
# Changelog:
# 1.0.3 - linting my ass off - enums to UPPER_CASE
"""

from enum import Enum


class LeagueEnum(Enum):
    """ MLE League Enumeration Class
    """
    PREMIER_LEAGUE = 1
    MASTER_LEAGUE = 2
    CHAMPION_LEAGUE = 3
    ACADEMY_LEAGUE = 4
    FOUNDATION_LEAGUE = 5
