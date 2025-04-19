"""provide methods to distribute sprocket data, such as players or franchises
    """
from __future__ import annotations


import difflib

from ... import const
from ...types import Member, SprocketLinks, PlayerRL, Franchise


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
    if discord_id:
        member: Member = lookup_rl(sprocket_data,
                                   discord_id=discord_id)
        if not member or not member.franchise:
            return None
        name = member.franchise['Franchise']

    return sprocket_data.franchise(name)


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
        member = sprocket_data.members.from_hash(str(discord_id))

    else:
        member = None

    if not member:
        return None

    player = sprocket_data.players.from_hash(member[const.SPR_HK_PLAYERS])
    if not player:
        return None

    return Member(member=member,
                  rl_player=PlayerRL(player=player,
                                     tracker=sprocket_data.trackers.from_hash(member['mle_id'])),
                  franchise=sprocket_data.teams.from_hash(player['franchise']))


def _get_member(sprocket_data: SprocketLinks,
                name: str,
                try_match: bool = False) -> dict:
    members = sprocket_data.members.data
    m = sprocket_data.members.from_secondary_hash(name)
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
