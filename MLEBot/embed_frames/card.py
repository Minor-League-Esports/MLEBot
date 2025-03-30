import os
import discord
from pydiscobot import frame, EmbedField


def mle_card(title: str,
             descr: str | None = None,
             franchise: dict | None = None,
             fields: list[EmbedField] | None = []) -> discord.Embed:
    """get generic Minor League E-Sports Embed 'card' for consistent formatting.

    Args:
        title (str): title of the embed
        descr (str | None, optional): description to add. Defaults to None.
        franchise (dict | None, optional): franchise for colouring & thumbnails. Defaults to None.

    Returns:
        discord.Embed: generic MLE formatted embed
    """
    color_str = os.getenv('MLE_COLOR') if not franchise else\
        franchise['Primary Color']

    url_str = os.getenv('MLE_LOGO_URL') if not franchise else\
        franchise['Photo URL']

    embed = frame(title,
                  descr,
                  fields,
                  color_str,
                  url_str)

    return embed
