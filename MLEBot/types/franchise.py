from dataclasses import dataclass
from .player import PlayerRL


@dataclass
class TeamRocketLeague:
    """Minor League E-Sports Rocket League Franchise Team
    """
    pl: list[PlayerRL]
    ml: list[PlayerRL]
    cl: list[PlayerRL]
    al: list[PlayerRL]
    fl: list[PlayerRL]

    def all_players(self):
        """get all players for this team

        Returns:
            list[PlayerRL]: all players
        """
        return self.pl + self.ml + self.cl + self.al + self.fl


@dataclass
class TeamTrackmania:
    """Minor League E-Sports Trackmania Franchise Team
    """
    cl: list[PlayerRL]
    al: list[PlayerRL]

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
