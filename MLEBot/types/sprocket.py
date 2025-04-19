"""Minor League E-Sports Franchise and Team Dataclasses
    """
from __future__ import annotations


from dataclasses import dataclass, field
from typing import Self


from .url_datalink import UrlDataLink
from .. import const


@dataclass
class PlayerRL:
    """MLE Sprocket Rocket League 'Player'
    """

    player: dict | None = None
    tracker: dict | None = None
    usage: dict | None = None

    @property
    def eligibility_date(self) -> str:
        """scrim point elgibility date

        Returns:
            str: eligible until:
        """
        return self.player["Eligible Until"]

    @property
    def eligible(self) -> bool:
        """eligible to play

        Returns:
            bool: eligible
        """
        return self.scrim_points >= 30

    @property
    def franchise(self) -> str:
        """player franchise

        Returns:
            str: franchise
        """
        return self.player["franchise"]

    @property
    def league(self) -> str:
        """player league (skill group)

        Returns:
            str: skill group
        """
        return self.skill_group

    @property
    def name(self) -> str:
        """player name

        Returns:
            str: name
        """
        return self.player["name"]

    @property
    def salary(self) -> str:
        """player salary

        Returns:
            str: salary
        """
        return self.player["salary"]

    @property
    def scrim_points(self) -> int:
        """scrim points

        Returns:
            str: current scrim points
        """
        return int(self.player["current_scrim_points"])

    @property
    def skill_group(self) -> str:
        """skill group

        Returns:
            str: skill group
        """
        return self.player["skill_group"]

    @property
    def slot(self) -> str:
        """player slot

        Returns:
            str: slot
        """
        return self.player["slot"]

    @property
    def staff_position(self) -> str:
        """franchise staff position

        Returns:
            str: franchise staff position
        """
        return self.player["Franchise Staff Position"]

    @property
    def usage_doubles(self) -> int:
        """player league usages
        doubles

        Returns:
            str: doubles usage
        """
        return int(self.usage["doubles_uses"])

    @property
    def usage_standard(self) -> int:
        """player league usages
        standard

        Returns:
            int: standard usage
        """
        return int(self.usage["standard_uses"])

    @property
    def usage_total(self) -> int:
        """player league usages
        total

        Returns:
            int: total usage
        """
        return int(self.usage['total_uses'])


@dataclass
class Member:
    """MLE Sprocket 'Member'
    """
    member: dict | None = None
    rl_player: PlayerRL = field(default_factory=PlayerRL())
    franchise: dict | None = None

    @property
    def mle_id(self) -> str:
        """member mle id

        Returns:
            str: mle id
        """
        return self.member['mle_id']

    @property
    def name(self) -> str:
        """member name

        Returns:
            str: name
        """
        return self.member['name']


class MLEFranchiseTeam(list[PlayerRL]):
    """sub team for MLE franchises (think 'ML' or 'AL')
    inherits list properties, used to add functions
    """

    def slot_sorted_players(self):
        """get all players sorted by slot
        """
        return sorted(self,
                      key=lambda x: x.slot)

    @classmethod
    def from_sprocket_data(cls,
                           players: list[dict],
                           trackers,
                           usages: list[dict]) -> Self:
        """compile list of PlayerRL from provided sprocket data
        consider hashing usages with role-league-team is the key or something?

        Args:
            players (list[dict]): sprocket players dict
            trackers (UrlDataLink): trackers link
            usages (list[dict]): usages dict

        Returns:
            Self: this class appended with a list of PlayerRL for this franchise
        """
        team = cls()
        team.extend([PlayerRL(x,
                              trackers.from_hash(x['member_id']),
                              next((y for y in usages if y['role'] == x['slot']), None))
                     for x in players])
        return team


@dataclass
class TeamRocketLeague:
    """Minor League E-Sports Rocket League Franchise Team
    """
    pl: MLEFranchiseTeam
    ml: MLEFranchiseTeam
    cl: MLEFranchiseTeam
    al: MLEFranchiseTeam
    fl: MLEFranchiseTeam

    def all_players(self):
        """get all players for this team

        Returns:
            list[PlayerRL]: all players
        """
        return self.pl + self.ml + self.cl + self.al + self.fl

    def by_skill_group(self,
                       skill_group: str) -> MLEFranchiseTeam:
        """get franchise team by skill group string

        Args:
            skill_group (str): sprocket const skill group

        Returns:
            MLEFranchiseTeam: team
        """
        match skill_group:
            case const.SPR_SG_PL:
                return self.pl
            case const.SPR_SG_ML:
                return self.ml
            case const.SPR_SG_CL:
                return self.cl
            case const.SPR_SG_AL:
                return self.al
            case const.SPR_SG_FL:
                return self.fl
            case _:
                return None


@dataclass
class TeamTrackmania:
    """Minor League E-Sports Trackmania Franchise Team
    """
    cl: MLEFranchiseTeam
    al: MLEFranchiseTeam

    def all_players(self):
        """get all players for this team

        Returns:
            list[PlayerRL]: all players
        """
        return self.cl + self.al


@dataclass
class Franchise:
    """Minor League E-Sports Franchise Dataclass
    """
    players_rl: TeamRocketLeague
    players_tm: TeamTrackmania
    franchise_meta: dict
    players_rl_meta: dict
    players_tm_meta: dict
    fm: dict
    gms: list[dict]
    agms: list[dict]
    captains: list[dict]
    pr: dict

    @classmethod
    def from_sprocket_links(cls,
                            meta_data: dict,
                            sprocket_data) -> Self:
        """compile franchise from sprocket links data

        Args:
            meta_data (dict): sprocket dict of the franchise to create
            sprocket_data (SprocketLinks): SprocketLinks class

        Returns:
            Self: Franchise class
        """

        # do data gathering here to keep the local def easy to read
        # gather rl data
        p_rl = [x for x in sprocket_data.players.data if x['franchise'] == meta_data['Franchise']]
        p_pl = [x for x in p_rl if x['skill_group'] == const.SPR_SG_PL and x['slot'] != 'NONE']
        p_ml = [x for x in p_rl if x['skill_group'] == const.SPR_SG_ML and x['slot'] != 'NONE']
        p_cl = [x for x in p_rl if x['skill_group'] == const.SPR_SG_CL and x['slot'] != 'NONE']
        p_al = [x for x in p_rl if x['skill_group'] == const.SPR_SG_AL and x['slot'] != 'NONE']
        p_fl = [x for x in p_rl if x['skill_group'] == const.SPR_SG_FL and x['slot'] != 'NONE']

        # usage data
        u_rl = [x for x in sprocket_data.usages.data if x['team_name'] == meta_data['Franchise']]
        u_pl = [x for x in u_rl if x['league'].lower() in const.SPR_SG_PL.lower()]
        u_ml = [x for x in u_rl if x['league'].lower() in const.SPR_SG_ML.lower()]
        u_cl = [x for x in u_rl if x['league'].lower() in const.SPR_SG_CL.lower()]
        u_al = [x for x in u_rl if x['league'].lower() in const.SPR_SG_AL.lower()]
        u_fl = [x for x in u_rl if x['league'].lower() in const.SPR_SG_FL.lower()]

        rl_team = TeamRocketLeague(
            pl=MLEFranchiseTeam.from_sprocket_data(p_pl,
                                                   sprocket_data.trackers,
                                                   u_pl),
            ml=MLEFranchiseTeam.from_sprocket_data(p_ml,
                                                   sprocket_data.trackers,
                                                   u_ml),
            cl=MLEFranchiseTeam.from_sprocket_data(p_cl,
                                                   sprocket_data.trackers,
                                                   u_cl),
            al=MLEFranchiseTeam.from_sprocket_data(p_al,
                                                   sprocket_data.trackers,
                                                   u_al),
            fl=MLEFranchiseTeam.from_sprocket_data(p_fl,
                                                   sprocket_data.trackers,
                                                   u_fl),
        )

        # gather tm data
        p_tm = []

        tm_team = TeamTrackmania(
            cl=MLEFranchiseTeam([]),
            al=MLEFranchiseTeam([])
        )

        # compile
        return cls(
            players_rl=rl_team,
            players_tm=tm_team,
            players_rl_meta=p_rl,
            players_tm_meta=p_tm,
            franchise_meta=meta_data,
            fm=next((x for x in p_rl if x['Franchise Staff Position'] == 'Franchise Manager'), None),
            gms=[x for x in p_rl if x['Franchise Staff Position'] == 'General Manager'],
            agms=[x for x in p_rl if x['Franchise Staff Position'] == 'Assistant General Manager'],
            captains=[x for x in p_rl if x['Franchise Staff Position'] == 'Captain'],
            pr=[x for x in p_rl if x['Franchise Staff Position'] == 'PR Support'],
        )

    @property
    def name(self) -> str:
        """franchise name

        Returns:
            str: franchise name
        """
        return self.franchise_meta['Franchise']

    def all_players(self) -> list[PlayerRL]:
        """get all players

        Returns:
            list[PlayerRL]: all players
        """
        return self.players_rl.all_players().extend(self.players_tm.all_players())

    def get_skill_group(self,
                        team: list[PlayerRL]) -> str | None:
        """cheap and easy get of skill group

        Args:
            team (list[PlayerRL]): team of players

        Returns:
            str: skill group
        """
        if len(team) != 0:
            return team[0].player['skill_group']
        return None


class SprocketLinks:
    """sprocket data links
    """

    def __init__(self):
        self.members: UrlDataLink = UrlDataLink('members', const.SPR_DL_MEMBERS, const.SPR_HK_MEMBERS,
                                                const.SPR_HK_MEMBERS_SECONDARY)
        self.players: UrlDataLink = UrlDataLink(
            'players', const.SPR_DL_PLAYERS, const.SPR_HK_PLAYERS)
        self.player_stats: UrlDataLink = UrlDataLink(
            'player_stats', const.SPR_DL_PLA_STATS, const.SPR_HK_PLA_STATS)
        self.scrims: UrlDataLink = UrlDataLink(
            'scrims', const.SPR_DL_SCRIMS, const.SPR_HK_SCRIMS)
        self.teams: UrlDataLink = UrlDataLink(
            'teams', const.SPR_DL_TEAMS, const.SPR_HK_TEAMS)
        self.fixtures: UrlDataLink = UrlDataLink(
            'fixtures', const.SPR_DL_FIXT, const.SPR_HK_FIXT)
        self.match_grps: UrlDataLink = UrlDataLink(
            'match_groups', const.SPR_DL_MAT_GRP, const.SPR_HK_MAT_GRP)
        self.matches: UrlDataLink = UrlDataLink(
            'matches', const.SPR_DL_MATCHES, const.SPR_HK_MATCHES)
        self.trackers: UrlDataLink = UrlDataLink(
            'trackers', const.SPR_DL_TRACKER, const.SPR_HK_TRACKER)
        self.usages: UrlDataLink = UrlDataLink(
            'usages', const.SPR_DL_USAGE, const.SPR_HK_USAGE)

        self._franchises: dict = {}

    def compile_data(self) -> None:
        """compile data (usually directly after updating all links)
        """
        if not self.teams.data:
            return

        for f in self.teams.data:
            self._franchises[f['Franchise'].lower()] = Franchise.from_sprocket_links(f,
                                                                                     self)

    def franchise(self,
                  name: str) -> franchise.Franchise | None:
        """get franchise by name

        Args:
            name (str): franchise name

        Returns:
            (Franchise | None): franchise or none
        """
        return self._franchises.get(name.lower(), None)

    def links(self):
        """get iterable links from this sprocket links class
        """
        return [getattr(self, x) for x in dir(self) if isinstance(getattr(self, x), UrlDataLink)]
