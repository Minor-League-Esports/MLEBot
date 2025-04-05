"""Minor League E-Sports Rocket League
    Team Eligibility Card
    """

from pydiscobot import EmbedField
from .card import mle_card
from ..services.const import SPR_INFO
from ..types import Franchise, MLEFranchiseTeam


def teameligibility_card(franchise: Franchise,
                         league: str):
    """Minor League E-Sports Rocket League
    Team Eligibility Card

    Args:
        franchise (dict): sprocket franchise
        players (dict): sprocket players dictionary

    Returns:
        discord.Embed: team usage card
    """
    title = f"**{franchise.name} Slot Usage Info**"
    descr = SPR_INFO

    fields: list[EmbedField] = []

    players: MLEFranchiseTeam = franchise.players_rl.by_skill_group(
        league).slot_sorted_players()

    if not players:
        fields.append(EmbedField(name='**Error**',
                                 value='An error has occured...'))
        return mle_card(title, descr, franchise.franchise_meta, fields)

    ljust_limit = 8

    for _p in players:
        fields.append(EmbedField(name=f"**{_p.name}**",
                                 value=f"`{'Role:'.ljust(ljust_limit)}` {_p.slot}\n"
                                 f"`{'Salary:'.ljust(ljust_limit)}` {_p.salary}\n"
                                 f"`{'Points:'.ljust(ljust_limit)}` {str(_p.scrim_points)}\n"
                                 f"`{'Until:'.ljust(ljust_limit)}` {_p.eligibility_date}"))

    return mle_card(title, descr, franchise.franchise_meta, fields)
