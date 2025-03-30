from dataclasses import dataclass, field
from .player import PlayerRL


@dataclass
class Member:
    """MLE Sprocket 'Member'
    """
    member: dict | None = None
    rl_player: PlayerRL = field(default_factory=PlayerRL())
    franchise: dict | None = None
