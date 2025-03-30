from pydiscobot import EmbedField
from .card import mle_card
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
    p = member.rl_player.player
    m = member.member
    tracker = member.rl_player.tracker
    franchise = member.franchise

    title = f"**{m['name']} Sprocket Info**"

    descr = 'Data gathered by sprocket public data links.\n'
    descr += 'See more at [sprocket links](https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html)\n'

    eligible = "`Yes`" if p['current_scrim_points'] >= 30 else "`No`"

    fields = [
        EmbedField('MLE Name', f"`{m['name']}`", True),
        EmbedField('MLE ID', f"`{m['mle_id']}`", True),
        EmbedField('Salary', f"`{p['salary']}`", True),
        EmbedField('League', f"`{p['skill_group']}`", True),
        EmbedField('Scrim Pts', f"`{p['current_scrim_points']}`", True),
        EmbedField('Eligible?', eligible, True),
        EmbedField('Franchise', f"`{p['franchise']}`", True),
        EmbedField('Staff?', f"`{p['Franchise Staff Position']}`", True),
        EmbedField('Role', f"`{p['slot']}`", True),
    ]

    if tracker:
        fields.append(EmbedField('**Tracker Link**', tracker['tracker']))

    embed = mle_card(title, descr, franchise, fields)

    return embed
