"""MLE Sprocket 'Member'
    """

from dataclasses import dataclass, field
from .player import PlayerRL


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
