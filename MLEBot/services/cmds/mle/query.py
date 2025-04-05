"""Lookup groups of players by provided filter.
    """

import discord
from discord import app_commands
from pydiscobot import InteractionPagination
from pydiscobot.types import Cmd
from ....embed_frames import mle_card
from ....services import const


class Query(Cmd):
    """Lookup groups of players by provided filter.
    """

    @app_commands.command(name='query',
                          description='Lookup groups of players by provided filter.')
    @app_commands.describe(league_filter='[PL, ML, CL, AL, FL]')
    @app_commands.describe(query_filter='[FA, RFA, Waivers, Pend]')
    @app_commands.describe(sorting='[salary, current_scrim_points, name]')
    @app_commands.choices(league_filter=[
        app_commands.Choice(name='PL', value=const.SPR_SG_PL),
        app_commands.Choice(name='ML', value=const.SPR_SG_ML),
        app_commands.Choice(name='CL', value=const.SPR_SG_CL),
        app_commands.Choice(name='AL', value=const.SPR_SG_AL),
        app_commands.Choice(name='FL', value=const.SPR_SG_FL)
    ],
        query_filter=[
            app_commands.Choice(name='FA', value='fa'),
            app_commands.Choice(name='RFA', value='rfa'),
            app_commands.Choice(name='Waivers', value='waivers'),
            app_commands.Choice(name='Pend', value='pend')
    ],
        sorting=[
            app_commands.Choice(name='Salary', value='salary'),
            app_commands.Choice(name='Scrim Points',
                                value='current_scrim_points'),
            app_commands.Choice(name='Name', value='name')
    ])
    @app_commands.default_permissions()
    async def query(self,
                    interaction: discord.Interaction,
                    league_filter: app_commands.Choice[str],
                    query_filter: str,
                    sorting: str) -> None:
        """query sprocket db with filters

        Args:
            interaction (discord.Interaction): interaction of query
            league_filter (app_commands.Choice[str]): which league?
            query_filter (str): which player pool?
            sorting (str): sorting type?
        """
        _players = sorted([x for x in self._parent.sprocket.links.players.data if x['franchise'].lower(
        ) == query_filter.lower() and x['skill_group'] == league_filter.value], key=lambda x: x[sorting], reverse=True)

        if len(_players) == 0:
            emb = mle_card('**Filtered Players**\n\n',
                           'There were no players to be found for this query!')
            await interaction.response.send_message(embed=emb)
            return

        async def get_page(page: int,
                           as_timout: bool = False):
            emb: discord.Embed = mle_card('**Filtered Players**\n\n',
                                          f'Players filtered for `{query_filter}`\n'
                                          f'Sorted by `{sorting}`')

            if as_timout:
                emb.add_field(name='**`Timeout`**',
                              value='This command has timed out. Type `[ub.help]` for help.')
                emb.set_footer(text='Page `1` of 1')
                return emb, 0

            elements_per_page = 15
            offset = (page - 1) * elements_per_page

            emb.add_field(name='**Sal      | Points |    Name**',
                          value='\n'.join(
                              [
                                  f"`{str(_p['salary']).ljust(4)} | {str(_p['current_scrim_points']).ljust(4)} | {_p['name']}`"
                                  for _p in _players[offset:offset + elements_per_page]]),
                          inline=False)

            total_pages = InteractionPagination.compute_total_pages(len(_players),
                                                                    elements_per_page)

            emb.set_footer(text=f'Page {page} of {total_pages}')
            return emb, total_pages

        await InteractionPagination(interaction, get_page).navigate()
