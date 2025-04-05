"""Minor League E-Sports Franchise and Team Dataclasses
    """

from dataclasses import dataclass
from typing import Self
from .player import PlayerRL
from ..services import const


class MLEFranchiseTeam(list[PlayerRL]):
    """sub team for MLE franchises (think 'ML' or 'AL')
    inherits list properties, used to add functions
    """

    def slot_sorted_players(self):
        """get all players sorted by slot
        """
        return sorted(self,
                      key=lambda x: x.slot)


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

        def _create_team(skill_group,
                         sprocket_data,
                         players,
                         usages) -> list[PlayerRL]:
            return [PlayerRL(x,
                             sprocket_data.trackers.from_hash(x['member_id']),
                             next((y for y in usages if y['role'] == x['slot'] and y['league'] == x['skill_group']), None))
                    for x in players if x['skill_group'] == skill_group and x['slot'] != 'NONE']

        # gather rl data
        p_rl = [x for x in sprocket_data.players.data if x['franchise'] == meta_data['Franchise']]
        u_rl = [x for x in sprocket_data.usages.data if x['team_name'] == meta_data['Franchise']]

        rl_team = TeamRocketLeague(
            pl=MLEFranchiseTeam(_create_team(
                const.SPR_SG_PL, sprocket_data, p_rl, u_rl)),
            ml=MLEFranchiseTeam(_create_team(
                const.SPR_SG_ML, sprocket_data, p_rl, u_rl)),
            cl=MLEFranchiseTeam(_create_team(
                const.SPR_SG_CL, sprocket_data, p_rl, u_rl)),
            al=MLEFranchiseTeam(_create_team(
                const.SPR_SG_AL, sprocket_data, p_rl, u_rl)),
            fl=MLEFranchiseTeam(_create_team(
                const.SPR_SG_FL, sprocket_data, p_rl, u_rl)),
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
            fm=next(
                (x for x in p_rl if x['Franchise Staff Position'] == 'Franchise Manager'), None),
            gms=[x for x in p_rl if x['Franchise Staff Position']
                 == 'General Manager'],
            agms=[x for x in p_rl if x['Franchise Staff Position']
                  == 'Assistant General Manager'],
            captains=[
                x for x in p_rl if x['Franchise Staff Position'] == 'Captain'],
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
