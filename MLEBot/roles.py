#!/usr/bin/env python
""" Discord Roles Module for use in Minor League E-Sports
# Author: irox_rl
# Purpose: General Functions of Discord Roles
# Version 1.0.2
"""

# local imports #
from enums import LeagueEnum

# non-local imports #
import copy
import discord
import os

""" Constants
"""
Aviators = "Aviators"
Bears = "Bears"
Blizzard = "Blizzard"
Bulls = "Bulls"
Comets = "Comets"
Demolition = "Demolition"
Dodgers = "Dodgers"
Ducks = "Ducks"
Eclipse = "Eclipse"
Elite = "Elite"
Express = "Express"
Flames = "Flames"
Foxes = "Foxes"
Hawks = "Hawks"
Hive = "Hive"
Hurricanes = "Hurricanes"
Jets = "Jets"
Knights = "Knights"
Lightning = "Lightning"
Outlaws = "Outlaws"
Pandas = "Pandas"
Pirates = "Pirates"
Puffins = "Puffins"
Rhinos = "Rhinos"
Sabres = "Sabres"
Shadow = "Shadow"
Sharks = "Sharks"
Spartans = "Spartans"
Spectre = "Spectre"
Tyrants = "Tyrants"
Waivers = "Waivers"
Wizards = "Wizards"
Wolves = "Wolves"
SOCIAL_MEDIA = 'Social Media'

# dotenv.load_dotenv('.env')
FRANCHISE_MANAGER = None
GENERAL_MANAGER_RL = None
GENERAL_MANAGER_TM = None
ASSISTANT_GENERAL_MANAGER_RL = None
ASSISTANT_GENERAL_MANAGER_TM = None
CAPTAIN = None
PREMIER_LEAGUE = None
MASTER_LEAGUE = None
CHAMPION_LEAGUE = None
ACADEMY_LEAGUE = None
FOUNDATION_LEAGUE = None
ROCKET_LEAGUE = None
PR_SUPPORT = None
FA = None
FP = None
Pend = None

ALL_MLE_ROLES = [
    Aviators,
    Bears,
    Blizzard,
    Bulls,
    Comets,
    Demolition,
    Dodgers,
    Ducks,
    Eclipse,
    Elite,
    Express,
    Flames,
    Foxes,
    Hawks,
    Hive,
    Hurricanes,
    Jets,
    Knights,
    Lightning,
    Outlaws,
    Pandas,
    Pirates,
    Puffins,
    Rhinos,
    Sabres,
    Shadow,
    Sharks,
    Spartans,
    Spectre,
    Tyrants,
    Waivers,
    Wizards,
    Wolves,
    FRANCHISE_MANAGER,
    GENERAL_MANAGER_RL,
    GENERAL_MANAGER_TM,
    ASSISTANT_GENERAL_MANAGER_RL,
    ASSISTANT_GENERAL_MANAGER_TM,
    CAPTAIN,
    PREMIER_LEAGUE,
    MASTER_LEAGUE,
    CHAMPION_LEAGUE,
    ACADEMY_LEAGUE,
    FOUNDATION_LEAGUE,
    ROCKET_LEAGUE,
    PR_SUPPORT,
    FA,
    FP,
    Pend,
]

ALL_TEAMS = [
    Aviators,
    Bears,
    Blizzard,
    Bulls,
    Comets,
    Demolition,
    Dodgers,
    Ducks,
    Eclipse,
    Elite,
    Express,
    Flames,
    Foxes,
    Hawks,
    Hive,
    Hurricanes,
    Jets,
    Knights,
    Lightning,
    Outlaws,
    Pandas,
    Pirates,
    Puffins,
    Rhinos,
    Sabres,
    Shadow,
    Sharks,
    Spartans,
    Spectre,
    Tyrants,
    Waivers,
    Wizards,
    Wolves,
]

FRANCHISE_ROLES = []
GENERAL_MGMT_ROLES = []
CAPTAIN_ROLES = []

""" Globals
"""
social_media: discord.Role | None = None
franchise_manager: discord.Role | None = None
general_manager_rl: discord.Role | None = None
general_manager_tm: discord.Role | None = None
assistant_general_manager_rl: discord.Role | None = None
assistant_general_manager_tm: discord.Role | None = None
captain: discord.Role | None = None
premier: discord.Role | None = None
master: discord.Role | None = None
champion: discord.Role | None = None
academy: discord.Role | None = None
foundation: discord.Role | None = None


def init(guild: discord.Guild):
    global social_media
    global franchise_manager
    global general_manager_rl
    global general_manager_tm
    global assistant_general_manager_rl
    global assistant_general_manager_tm
    global captain
    global premier
    global master
    global champion
    global academy
    global foundation
    global FRANCHISE_ROLES, GENERAL_MGMT_ROLES, CAPTAIN_ROLES
    global FRANCHISE_MANAGER, GENERAL_MANAGER_RL, GENERAL_MANAGER_TM, ASSISTANT_GENERAL_MANAGER_RL, ASSISTANT_GENERAL_MANAGER_TM
    global CAPTAIN, PREMIER_LEAGUE, MASTER_LEAGUE, CHAMPION_LEAGUE, ACADEMY_LEAGUE, FOUNDATION_LEAGUE

    FRANCHISE_MANAGER = os.getenv('ROLE_FM')
    GENERAL_MANAGER_RL = os.getenv('ROLE_GM_RL')
    GENERAL_MANAGER_TM = os.getenv('ROLE_GM_TM')
    ASSISTANT_GENERAL_MANAGER_RL = os.getenv('ROLE_AGM_RL')
    ASSISTANT_GENERAL_MANAGER_TM = os.getenv('ROLE_AGM_TM')
    CAPTAIN = os.getenv('ROLE_CAPTAIN_RL')
    PREMIER_LEAGUE = os.getenv('ROLE_PL')
    MASTER_LEAGUE = os.getenv('ROLE_ML')
    CHAMPION_LEAGUE = os.getenv('ROLE_CL')
    ACADEMY_LEAGUE = os.getenv('ROLE_AL')
    FOUNDATION_LEAGUE = os.getenv('ROLE_FL')

    social_media = get_role_by_name(guild, SOCIAL_MEDIA)
    franchise_manager = get_role_by_name(guild, FRANCHISE_MANAGER)
    general_manager_rl = get_role_by_name(guild, GENERAL_MANAGER_RL)
    general_manager_tm = get_role_by_name(guild, GENERAL_MANAGER_TM)
    assistant_general_manager_rl = get_role_by_name(guild, ASSISTANT_GENERAL_MANAGER_RL)
    assistant_general_manager_tm = get_role_by_name(guild, ASSISTANT_GENERAL_MANAGER_TM)
    captain = get_role_by_name(guild, CAPTAIN)
    premier = get_role_by_name(guild, PREMIER_LEAGUE)
    master = get_role_by_name(guild, MASTER_LEAGUE)
    champion = get_role_by_name(guild, CHAMPION_LEAGUE)
    academy = get_role_by_name(guild, ACADEMY_LEAGUE)
    foundation = get_role_by_name(guild, FOUNDATION_LEAGUE)

    FRANCHISE_ROLES = [franchise_manager,
                       general_manager_rl,
                       general_manager_tm,
                       assistant_general_manager_rl,
                       assistant_general_manager_tm,
                       captain,
                       premier,
                       master,
                       champion,
                       academy,
                       foundation,
                       social_media]

    GENERAL_MGMT_ROLES = [franchise_manager,
                          general_manager_rl,
                          general_manager_tm,
                          assistant_general_manager_rl,
                          assistant_general_manager_tm]

    CAPTAIN_ROLES = copy.copy(GENERAL_MGMT_ROLES)
    CAPTAIN_ROLES.append(captain)


def get_role_by_name(guild: discord.Guild, name: str) -> discord.Role | None:
    return next((x for x in guild.roles if x.name == name), None)


def get_role_by_league(self, league: LeagueEnum):
    match league:
        case LeagueEnum.Premier_League:
            return self.premier
        case LeagueEnum.Master_League:
            return self.master
        case LeagueEnum.Champion_League:
            return self.champion
        case LeagueEnum.Academy_League:
            return self.academy
        case LeagueEnum.Foundation_League:
            return self.foundation


def has_role(member: discord.user, *roles) -> bool:
    return next((True for role in roles if role in member.roles), False)


def resolve_sprocket_league_role(sprocket_league: str) -> str | None:
    if sprocket_league == 'FOUNDATION':
        return FOUNDATION_LEAGUE
    if sprocket_league == 'ACADEMY':
        return ACADEMY_LEAGUE
    if sprocket_league == 'CHAMPION':
        return CHAMPION_LEAGUE
    if sprocket_league == 'MASTER':
        return MASTER_LEAGUE
    if sprocket_league == 'PREMIER':
        return PREMIER_LEAGUE
    return None
