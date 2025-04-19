"""frames module for MLEBot
    """
from __future__ import annotations


import os


import discord


from pydiscobot import (
    frame,
    EmbedField,
)


from . import const
from .types.sprocket import Member, Franchise, PlayerRL, MLEFranchiseTeam


def mle_card(title: str,
             descr: str | None = None,
             franchise: dict | None = None,
             fields: list[EmbedField] | None = None) -> discord.Embed:
    """get generic Minor League E-Sports Embed 'card' for consistent formatting.

    Args:
        title (str): title of the embed
        descr (str | None, optional): description to add. Defaults to None.
        franchise (dict | None, optional): franchise for colouring & thumbnails. Defaults to None.

    Returns:
        discord.Embed: generic MLE formatted embed
    """
    if not fields:
        fields = []

    color_str = os.getenv('MLE_COLOR') if not franchise else\
        franchise['Primary Color']

    url_str = os.getenv('MLE_LOGO_URL') if not franchise else\
        franchise['Photo URL']

    embed = frame.get_frame(title,
                            descr,
                            fields,
                            color_str,
                            url_str)

    return embed


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

    descr = const.SPR_INFO

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
    descr = const.SPR_INFO

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


def teaminfo_card(franchise: Franchise):
    """Minor League E-Sports Rocket League
    Team Info Card

    Args:
        franchise (dict): sprocket franchise

    Returns:
        discord.Embed: team info card
    """
    title = f"{franchise.name} Roster"
    descr = const.SPR_INFO

    fields = [
        EmbedField('**Franchise Manager**',
                   f"`{franchise.fm['name']}`" if franchise.fm else "N/A"),
        EmbedField('**General Managers**',
                   "\n".join([f"`{gm['name']}`" for gm in franchise.gms])),
    ]

    if len(franchise.agms) > 0:
        fields.append(EmbedField('**Assistant General Managers**',
                                 "\n".join([f"`{agm['name']}`" for agm in franchise.agms])))

    if len(franchise.captains) > 0:
        fields.append(EmbedField('**Captains**',
                                 "\n".join([f"`{x['name']}`" for x in franchise.captains])))

    if len(franchise.pr) > 0:
        fields.append(EmbedField('**PR Supports**',
                                 "\n".join([f"`{x['name']}`" for x in franchise.pr])))

    def _team_info(players: list[PlayerRL],
                   league_name: str,
                   salary_cap: float) -> list[EmbedField]:
        if not players:
            return None

        @staticmethod
        def _player_info(p) -> str | None:
            """get string of info for player"""
            slot = p['slot'].removeprefix('PLAYER')
            return f"`{slot} | {p['salary']} | {p['name']}`"

        def _team_salary(players: list[PlayerRL],
                         league_name: str,
                         salary_cap: float) -> str:
            top_sals = sorted(players,
                              key=lambda p: p.player['salary'],
                              reverse=True)
            sal_ceiling = 0.0
            range_length = 5 if len(top_sals) >= 5 else len(top_sals)
            for i in range(range_length):
                sal_ceiling += top_sals[i].player['salary']
            _signable_str = f"+{top_sals[-1].player['salary'] + (salary_cap - sal_ceiling)}" if sal_ceiling <= salary_cap else "NONE"
            return f'**`[{sal_ceiling} / {salary_cap}] [{_signable_str}]` {league_name}**'

        fields: list[EmbedField] = []
        players_strings = '\n'.join(
            [_player_info(player.player) for player in players if player.player is not None])

        fields.append(EmbedField(name=_team_salary(players,
                                                   league_name,
                                                   salary_cap),
                                 value=players_strings))
        return fields

    fields.append(EmbedField('**Roster**',
                             '**`[Top5/SalCap] [CanSign] League`**'))

    pl = _team_info(franchise.players_rl.pl.slot_sorted_players(),
                    const.SPR_SG_PL,
                    const.SALARY_CAP_PL)
    ml = _team_info(franchise.players_rl.ml.slot_sorted_players(),
                    const.SPR_SG_ML,
                    const.SALARY_CAP_ML)
    cl = _team_info(franchise.players_rl.cl.slot_sorted_players(),
                    const.SPR_SG_CL,
                    const.SALARY_CAP_CL)
    al = _team_info(franchise.players_rl.al.slot_sorted_players(),
                    const.SPR_SG_AL,
                    const.SALARY_CAP_AL)
    fl = _team_info(franchise.players_rl.fl.slot_sorted_players(),
                    const.SPR_SG_FL,
                    const.SALARY_CAP_FL)
    if pl:
        fields.extend(pl)
    if ml:
        fields.extend(ml)
    if cl:
        fields.extend(cl)
    if al:
        fields.extend(al)
    if fl:
        fields.extend(fl)

    return mle_card(title,
                    descr,
                    franchise.franchise_meta,
                    fields)


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
