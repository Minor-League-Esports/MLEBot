"""salary card
    display player league information
    """

from pydiscobot import EmbedField
from .card import mle_card
from ..services.const import SPR_INFO
from ..types import Member


def salary_card(member: Member):
    """Minor League E-Sports Rocket League Player
    Salary Card

    Args:
        member (dict): sprocket member
        player (dict): sprocket player
        franchise (dict): sprocket franchise
        tracker (dict): sprocket tracker

    Returns:
        discord.Embed: salary card for specified player
    """
    player = member.rl_player
    tracker = member.rl_player.tracker

    title = f"**{member.name} Sprocket Info**"

    descr = SPR_INFO

    fields = [
        EmbedField('MLE Name', f"`{member.name}`", True),
        EmbedField('MLE ID', f"`{member.mle_id}`", True),
        EmbedField('Salary', f"`{player.salary}`", True),
        EmbedField('League', f"`{player.skill_group}`", True),
        EmbedField('Scrim Pts', f"`{player.scrim_points}`", True),
        EmbedField('Eligible?', "`Yes`" if player.eligible else "`No`", True),
        EmbedField('Franchise', f"`{player.franchise}`", True),
        EmbedField('Staff?', f"`{player.staff_position}`", True),
        EmbedField('Role', f"`{player.slot}`", True),
    ]

    if tracker:
        fields.append(EmbedField('**Tracker Link**',
                      member.rl_player.tracker['tracker']))

    embed = mle_card(title, descr, member.franchise, fields)

    return embed
