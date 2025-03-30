import difflib
from ...services import const
from ...types import Member, SprocketLinks, PlayerRL, Franchise, TeamRocketLeague, TeamTrackmania


def lookup_franchise(sprocket_data: SprocketLinks,
                     name: str | None = None,
                     discord_id: str | int | None = None) -> Franchise | None:
    """lookup franchise from sprocket

    Args:
        sprocket_data (SprocketLinks): sprocket data
        discord_id (str | int | None): discord id of user

    Returns:
        Franchise | None: _description_
    """
    franchise: dict | None = None

    if discord_id:
        member: Member = lookup_rl(sprocket_data,
                                   discord_id=discord_id)
        if not member or not member.franchise:
            return None
        franchise = member.franchise
    elif name:
        franchise = _get_franchise(sprocket_data,
                                   name=name)
        if not franchise:
            return None

    else:
        return None

    # gather rl data
    p_rl = [x for x in sprocket_data.players.data if x['franchise']
            == franchise['Franchise']]

    pl = [PlayerRL(x,
                   next((y for y in sprocket_data.trackers.data if y['mleid'] == x['member_id']), None),
                   next((y for y in sprocket_data.usages.data if y['role'] == x['slot']), None))
          for x in p_rl if x['skill_group'] == const.SPR_SG_PL and x['slot'] != 'NONE']

    ml = [PlayerRL(x,
                   next((y for y in sprocket_data.trackers.data if y['mleid'] == x['member_id']), None),
                   next((y for y in sprocket_data.usages.data if y['role'] == x['slot']), None))
          for x in p_rl if x['skill_group'] == const.SPR_SG_ML and x['slot'] != 'NONE']

    cl = [PlayerRL(x,
                   next((y for y in sprocket_data.trackers.data if y['mleid'] == x['member_id']), None),
                   next((y for y in sprocket_data.usages.data if y['role'] == x['slot']), None))
          for x in p_rl if x['skill_group'] == const.SPR_SG_CL and x['slot'] != 'NONE']

    al = [PlayerRL(x,
                   next((y for y in sprocket_data.trackers.data if y['mleid'] == x['member_id']), None),
                   next((y for y in sprocket_data.usages.data if y['role'] == x['slot']), None))
          for x in p_rl if x['skill_group'] == const.SPR_SG_AL and x['slot'] != 'NONE']

    fl = [PlayerRL(x,
                   next((y for y in sprocket_data.trackers.data if y['mleid'] == x['member_id']), None),
                   next((y for y in sprocket_data.usages.data if y['role'] == x['slot']), None))
          for x in p_rl if x['skill_group'] == const.SPR_SG_FL and x['slot'] != 'NONE']

    rl_team = TeamRocketLeague(
        pl=pl,
        ml=ml,
        cl=cl,
        al=al,
        fl=fl,
    )

    # gather tm data
    p_tm = []

    tm_team = TeamTrackmania(
        cl=[],
        al=[]
    )

    # compile
    return Franchise(
        players_rl=rl_team,
        players_tm=tm_team,
        players_rl_meta=p_rl,
        players_tm_meta=p_tm,
        franchise_meta=franchise,
        fm=next((x for x in p_rl if x['Franchise Staff Position'] == 'Franchise Manager'), None),
        gms=[x for x in p_rl if x['Franchise Staff Position'] == 'General Manager'],
        agms=[x for x in p_rl if x['Franchise Staff Position'] == 'Assistant General Manager'],
        captains=[x for x in p_rl if x['Franchise Staff Position'] == 'Captain'],
        pr=[x for x in p_rl if x['Franchise Staff Position'] == 'PR Support'],
    )


def lookup_rl(sprocket_data: SprocketLinks,
              name: str | None = None,
              discord_id: str | int | None = None) -> Member | None:
    """lookup a rocket league player from sprocket

    Args:
        sprocket_data (SprocketLinks): sprocket data links supplied by bot
        name (str): name of player to look up

    Returns:
        Member | None: _description_
    """
    if not name and not discord_id:
        return None

    if name:
        member = _get_member(sprocket_data, name, try_match=True)
    elif discord_id:
        member = _get_id_member(sprocket_data, discord_id)
    else:
        member = None

    if not member:
        return None

    player = _get_player(sprocket_data, member)
    if not player:
        return None

    return Member(member=member,
                  rl_player=PlayerRL(player=player,
                                     tracker=_get_tracker(sprocket_data, member)),
                  franchise=_get_franchise(sprocket_data, player))


def _get_member(sprocket_data: SprocketLinks,
                name: str,
                try_match: bool = False) -> dict:
    members = sprocket_data.members.data
    m = next((x for x in members if x['name'].lower() == name.lower()), None)
    if not m and try_match:
        matches = difflib.get_close_matches(name,
                                            [x['name'] for x in members],
                                            1)
        if matches:
            m = next(
                (x for x in members if x['name'].lower()
                 == matches[0].lower()),
                None)
    return m


def _get_id_member(sprocket_data: SprocketLinks,
                   discord_id: int | str):
    members = sprocket_data.members.data
    return next((x for x in members if x['discord_id'] == str(discord_id)), None)


def _get_player(sprocket_data: SprocketLinks,
                member: dict):
    players = sprocket_data.players.data
    return next((x for x in players if x['member_id'] == member['member_id']),
                None)


def _get_franchise(sprocket_data: SprocketLinks,
                   player: dict | None = None,
                   name: str | None = None):
    franchises = sprocket_data.teams.data

    if player:
        return next((x for x in franchises if x['Franchise'] == player['franchise']),
                    None)
    elif name:
        return next((x for x in franchises if x['Franchise'].lower() == name.lower()),
                    None)
    else:
        return None


def _get_tracker(sprocket_data: SprocketLinks,
                 member: dict):
    trackers = sprocket_data.trackers.data
    return next((x for x in trackers if x['mleid'] == member['mle_id']),
                None)
