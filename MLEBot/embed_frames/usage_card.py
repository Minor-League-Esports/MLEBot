from pydiscobot import EmbedField
from .card import mle_card
from ..types import Franchise, PlayerRL
from ..services import const


def usage_card(franchise: Franchise):
    """Minor League E-Sports Rocket League
    Usage Card

    Args:
        franchise (dict): sprocket franchise
        players (dict): sprocket players dictionary

    Returns:
        discord.Embed: team usage card
    """
    title = f"**{franchise.name} Slot Usage Info**"
    descr = const.SPR_INFO

    fields = [
        EmbedField('**Season Slot Allowances**',
                   f'`Dbl: {const.SLOT_USAGE_DBL} | Std: {const.SLOT_USAGE_STD} | Ttl: {const.SLOT_USAGE_TTL}`')
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
    slot = player.slot.removeprefix('PLAYER')
    dbl_use = player.usage_doubles
    std_use = player.usage_standard
    ttl_use = player.usage_total
    name = player.name
    return f"`{slot} 2s: {dbl_use} | 3s: {std_use} | All: {ttl_use} | {name}`"
