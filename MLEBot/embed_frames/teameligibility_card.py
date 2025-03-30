from pydiscobot import EmbedField
from .card import mle_card
from ..types import Franchise


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
    title = f"**{franchise.franchise_meta['Franchise']} Slot Usage Info**"
    descr = 'Data gathered by sprocket public data links.\n'
    descr += 'See more at [sprocket links](https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html)\n'

    fields = [
        EmbedField('**Season Slot Allowances**',
                   '`Doubles: 6 | Standard: 8 | Total: 12`   ')
    ]

    players = sorted([x for x in franchise.players_rl.all_players() if x.player['skill_group'] == league],
                     key=lambda x: x.player['slot'])

    if not players:
        fields.append(EmbedField(name='**Error**',
                                 value='An error has occured...'))
        return mle_card(title, descr, franchise.franchise_meta, fields)

    ljust_limit = 8

    for _p in players:
        fields.append(EmbedField(name=f"**{_p.player['name']}**",
                                 value=f"`{'Role:'.ljust(ljust_limit)}` {_p.player['slot']}\n"
                                 f"`{'Salary:'.ljust(ljust_limit)}` {_p.player['salary']}\n"
                                 f"`{'Points:'.ljust(ljust_limit)}` {str(_p.player['current_scrim_points'])}\n"
                                 f"`{'Until:'.ljust(ljust_limit)}` {str(_p.player['Eligible Until'])}"))

    return mle_card(title, descr, franchise.franchise_meta, fields)
