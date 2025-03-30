from pydiscobot import EmbedField
from .card import mle_card
from ..types import Franchise, PlayerRL


def usage_card(franchise: Franchise):
    """Minor League E-Sports Rocket League
    Usage Card

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

    if franchise.players_rl.pl:
        fields.append(EmbedField(
            name='Premier',
            value='\n'.join([_player_usage_string(x)
                            for x in franchise.players_rl.pl])))

    if franchise.players_rl.ml:
        fields.append(EmbedField(
            name='Master',
            value='\n'.join([_player_usage_string(x)
                            for x in franchise.players_rl.ml])))

    if franchise.players_rl.cl:
        fields.append(EmbedField(
            name='Champion',
            value='\n'.join([_player_usage_string(x)
                            for x in franchise.players_rl.cl])))

    if franchise.players_rl.al:
        fields.append(EmbedField(
            name='Academy',
            value='\n'.join([_player_usage_string(x)
                            for x in franchise.players_rl.al])))

    if franchise.players_rl.fl:
        fields.append(EmbedField(
            name='Foundation',
            value='\n'.join([_player_usage_string(x)
                            for x in franchise.players_rl.fl])))

    return mle_card(title, descr, franchise.franchise_meta, fields)


def _player_usage_string(player: PlayerRL):
    slot = player.player['slot'].removeprefix('PLAYER')
    dbl_use = player.usage['doubles_uses']
    std_use = player.usage['standard_uses']
    ttl_use = player.usage['total_uses']
    name = player.player['name']
    return f"`{slot} 2s: {dbl_use} | 3s: {std_use} | All: {ttl_use} | {name}`"
