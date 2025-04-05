"""Minor League E-Sports Rocket League
    Team Info Card
    """

from pydiscobot import EmbedField
from .card import mle_card
from ..types import Franchise, PlayerRL
from ..services import const


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
