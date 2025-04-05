"""Minor League E-Sports Franchise and Team Dataclasses
    """

from dataclasses import dataclass
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
                        team: list[PlayerRL]) -> str:
        """cheap and easy get of skill group

        Args:
            team (list[PlayerRL]): team of players

        Returns:
            str: skill group
        """
        if len(team) != 0:
            return team[0].player['skill_group']
