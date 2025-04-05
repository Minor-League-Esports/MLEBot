"""MLE Sprocket Rocket League 'Player'
    """

from dataclasses import dataclass


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
