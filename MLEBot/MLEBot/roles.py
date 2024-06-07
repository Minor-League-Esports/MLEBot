""" Discord Roles Module for use in Minor League E-Sports
# Author: irox_rl
# Purpose: General Functions of Discord Roles
"""
import copy
import discord
import enums
import member

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
FRANCHISE_MANAGER = 'Franchise Manager'
GENERAL_MANAGER_RL = 'GM Rocket League'
GENERAL_MANAGER_TM = 'GM Trackmania'
ASSISTANT_GENERAL_MANAGER_RL = 'AGM Rocket League'
ASSISTANT_GENERAL_MANAGER_TM = 'AGM Trackmania'
CAPTAIN = 'Captain Rocket League'
PREMIER_LEAGUE = 'Premier League'
MASTER_LEAGUE = 'Master League'
CHAMPION_LEAGUE = 'Champion League'
ACADEMY_LEAGUE = 'Academy League'
FOUNDATION_LEAGUE = 'Foundation League'
ROCKET_LEAGUE = 'Rocket League'
PR_SUPPORT = 'PR Support'
FA = 'Free Agent'
FP = 'Former Player'
Pend = 'Pending FA'

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
    global GENERAL_MGMT_ROLES, CAPTAIN_ROLES

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

    GENERAL_MGMT_ROLES = [franchise_manager,
                          general_manager_rl,
                          general_manager_tm,
                          assistant_general_manager_rl,
                          assistant_general_manager_tm]

    CAPTAIN_ROLES = copy.copy(GENERAL_MGMT_ROLES)
    CAPTAIN_ROLES.append(captain)


def get_role_by_name(guild: discord.Guild, name: str) -> discord.Role | None:
    return next((x for x in guild.roles if x.name == name), None)


def get_role_by_league(self, league: enums.LeagueEnum):
    match league:
        case enums.LeagueEnum.Premier_League:
            return self.premier
        case enums.LeagueEnum.Master_League:
            return self.master
        case enums.LeagueEnum.Champion_League:
            return self.champion
        case enums.LeagueEnum.Academy_League:
            return self.academy
        case enums.LeagueEnum.Foundation_League:
            return self.foundation


def has_role(_member: discord.user, *roles) -> bool:
    return member.has_role(_member, *roles)


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
