from dataclasses import dataclass


@dataclass
class PlayerRL:
    """MLE Sprocket Rocket League 'Player'
    """
    player: dict | None = None
    tracker: dict | None = None
    usage: dict | None = None
