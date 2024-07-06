#!/usr/bin/env python
""" Minor League E-Sports Team
# Author: irox_rl
# Purpose: General Functions of a League Team
# Version 1.0.4
"""

from PyDiscoBot import channels, err

# local imports #
from member import Member
from enums import LeagueEnum

# non-local imports #
import os
import datetime
import discord
from discord.ext import commands
from html2image import Html2Image

MLE_SEASON = 'Season 17'
EMOTE_CHECK_GREEN = ':white_check_mark:'
EMOTE_X_RED = ':x:'
EMOTE_SABRES_NO_BG_ID = '1002420732837511248'


class Team:
    """ Minor League E-Sports Team Class\n
        """

    def __init__(self,
                 guild: discord.Guild,
                 franchise,
                 league: LeagueEnum) -> None:
        """ Initialize method\n
            **param master_bot**: reference to mle_bot Bot class that is running this repo\n
            **param team_name**: string representation of this team's name (e.g. **'Sabres'**)\n
            **param league**: enumeration of the league this team belongs to\n
            All data is initialized to zero. Update method must be called with proper sprocket data to get actual statistics for this class\n
            For additional information about Sprocket Data Sets and these dictionaries, see:\n
            https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html
        """
        self.guild = guild
        self.franchise = franchise
        self.league = league
        self.players: [Member] = []
        self.channel: discord.TextChannel | None = None
        self.message: discord.Message | None = None
        self.message_id = None
        self.played_matches: [{}] = None
        self.sprocket_data: {} = None
        self.standard_series_wins = 0
        self.standard_series_losses = 0
        self.standard_wins = 0
        self.standard_losses = 0
        self.doubles_series_wins = 0
        self.doubles_series_losses = 0
        self.doubles_wins = 0
        self.doubles_losses = 0
        self._sprocket_players: [{}] = []
        self._sprocket_members: [{}] = []

    @property
    def league_name(self) -> str:
        return self.league.name.replace('_', ' ')

    @property
    def sprocket_members(self):
        return self._sprocket_members

    @property
    def sprocket_players(self):
        return self._sprocket_players

    def __get_emote_by_id__(self, emoji_id: str) -> discord.Emoji | None:
        """ helper function to get guild emote by supplied ID\n
            ***returns***: discord emote or None"""
        return next((x for x in self.guild.emojis if x.id.__str__() == emoji_id), None)

    def __get_weekly_info__(self, game_mode: str, match_week: str) -> {}:
        """ Helper function to get a dictionary describing the match of a specified game mode from a specific week\n
                        **param game_mode**: specified game mode that is being posted ('Standard' or 'Doubles')\n
                        **param match_week**: specified match_week that is being posted ('Match 1', e.g.)\n
                        **returns** dictionary describing the match\n
                        """
        sprocket_data = self.franchise.bot.sprocket.data
        """ Using stored sprocket data, get match groups of this specified week / season
        """
        match_group_weeks = [x for x in sprocket_data['sprocket_match_groups'] if
                             x['match_group_title'] == match_week and x['parent_group_title'] == os.getenv('SEASON')]

        """ Get the match from the specified week / specified mode of this season
        """
        match_this_week = next((x for x in self.played_matches for y in match_group_weeks if
                                x['match_group_id'] == y['match_group_id'] and x['game_mode'] == game_mode), None)

        """ If we didn't get a match for this week, return an empty dictionary
        """
        if not match_this_week:
            return {
                'home_team': '',
                'away_team': '',
                'score': '',
                'home_color': '',
                'away_color': '',
                'home_url': '',
                'away_url': '',
            }

        """ Gather both teams from the match
        """
        team1 = next((x for x in sprocket_data['sprocket_teams'] if x['name'] == match_this_week['home']), None)
        team2 = next((x for x in sprocket_data['sprocket_teams'] if x['name'] == match_this_week['away']), None)

        """ If BOTH teams weren't found, return an empty dictionary
        """
        if (not team1) or (not team2):
            return {
                'home_team': '',
                'away_team': '',
                'score': '',
                'home_color': '',
                'away_color': '',
                'home_url': '',
                'away_url': '',
            }

        """ Get the scores
        """
        hm_score = match_this_week['home_wins']
        away_score = match_this_week['away_wins']
        score_wk = f'{hm_score} - {away_score}'

        """ Assemble all the data into a dictionary and return
        """
        return {
            'home_team': match_this_week['home'],
            'away_team': match_this_week['away'],
            'score': score_wk,
            'home_color': team1['primary_color'],
            'away_color': team2['secondary_color'],
            'home_url': team1['logo_img_link'],
            'away_url': team2['logo_img_link'],
        }

    async def __post_quick_info_html__(self, ctx: discord.ext.commands.Context | discord.TextChannel | None = None):
        """ Helper function to post quick info html to the quick info channel of this team\n
                        **`optional`param ctx**: specified context to send information to. If not supplied, the info is posted to the team's quick info channel.\n
                        **returns** None\n
                        """
        """ Parse all possible players based on role as defined by MLE
        """
        playerA: Member | None = next((x for x in self.players if x.role == 'PLAYERA'), None)
        playerB: Member | None = next((x for x in self.players if x.role == 'PLAYERB'), None)
        playerC: Member | None = next((x for x in self.players if x.role == 'PLAYERC'), None)
        playerD: Member | None = next((x for x in self.players if x.role == 'PLAYERD'), None)
        playerE: Member | None = next((x for x in self.players if x.role == 'PLAYERE'), None)
        playerF: Member | None = next((x for x in self.players if x.role == 'PLAYERF'), None)
        playerG: Member | None = next((x for x in self.players if x.role == 'PLAYERG'), None)
        playerH: Member | None = next((x for x in self.players if x.role == 'PLAYERH'), None)
        playerA_name = next((x.mle_name for x in self.players if x.role == 'PLAYERA'), '')
        playerB_name = next((x.mle_name for x in self.players if x.role == 'PLAYERB'), '')
        playerC_name = next((x.mle_name for x in self.players if x.role == 'PLAYERC'), '')
        playerD_name = next((x.mle_name for x in self.players if x.role == 'PLAYERD'), '')
        playerE_name = next((x.mle_name for x in self.players if x.role == 'PLAYERE'), '')
        playerF_name = next((x.mle_name for x in self.players if x.role == 'PLAYERF'), '')
        playerG_name = next((x.mle_name for x in self.players if x.role == 'PLAYERG'), '')
        playerH_name = next((x.mle_name for x in self.players if x.role == 'PLAYERH'), '')

        """ Can we fix this to not use my local stuff please... god i'm an idiot
        """
        if playerA:
            playerA_emote = 'D:\Personal\SabresUtilityBot\checkmark.png' if playerA.schedule_confirmed else 'D:\Personal\SabresUtilityBot\\redex.png'
        else:
            playerA_emote = None
        if playerB:
            playerB_emote = 'D:\Personal\SabresUtilityBot\checkmark.png' if playerB.schedule_confirmed else 'D:\Personal\SabresUtilityBot\\redex.png'
        else:
            playerB_emote = None
        if playerC:
            playerC_emote = 'D:\Personal\SabresUtilityBot\checkmark.png' if playerC.schedule_confirmed else 'D:\Personal\SabresUtilityBot\\redex.png'
        else:
            playerC_emote = None
        if playerD:
            playerD_emote = 'D:\Personal\SabresUtilityBot\checkmark.png' if playerD.schedule_confirmed else 'D:\Personal\SabresUtilityBot\\redex.png'
        else:
            playerD_emote = None
        if playerE:
            playerE_emote = 'D:\Personal\SabresUtilityBot\checkmark.png' if playerE.schedule_confirmed else 'D:\Personal\SabresUtilityBot\\redex.png'
        else:
            playerE_emote = None
        if playerF:
            playerF_emote = 'D:\Personal\SabresUtilityBot\checkmark.png' if playerF.schedule_confirmed else 'D:\Personal\SabresUtilityBot\\redex.png'
        else:
            playerF_emote = None
        if playerG:
            playerG_emote = 'D:\Personal\SabresUtilityBot\checkmark.png' if playerG.schedule_confirmed else 'D:\Personal\SabresUtilityBot\\redex.png'
        else:
            playerG_emote = None
        if playerH:
            playerH_emote = 'D:\Personal\SabresUtilityBot\checkmark.png' if playerH.schedule_confirmed else 'D:\Personal\SabresUtilityBot\\redex.png'
        else:
            playerH_emote = None

        hti = Html2Image(size=(615, 695))
        html_string = open('..\TeamQuickInfo.html').read().format(league=get_league_text(self.league),
                                                                  std_series_wins=self.standard_series_wins,
                                                                  std_series_losses=self.standard_series_losses,
                                                                  std_game_wins=self.standard_wins,
                                                                  std_game_losses=self.standard_losses,
                                                                  dbl_series_wins=self.doubles_series_wins,
                                                                  dbl_series_losses=self.doubles_series_losses,
                                                                  dbl_game_wins=self.doubles_wins,
                                                                  dbl_game_losses=self.doubles_losses,
                                                                  player_a_mle_name=playerA_name,
                                                                  player_a_emote=playerA_emote,
                                                                  player_b_mle_name=playerB_name,
                                                                  player_b_emote=playerB_emote,
                                                                  player_c_mle_name=playerC_name,
                                                                  player_c_emote=playerC_emote,
                                                                  player_d_mle_name=playerD_name,
                                                                  player_d_emote=playerD_emote,
                                                                  player_e_mle_name=playerE_name,
                                                                  player_e_emote=playerE_emote,
                                                                  player_f_mle_name=playerF_name,
                                                                  player_f_emote=playerF_emote,
                                                                  player_g_mle_name=playerG_name,
                                                                  player_g_emote=playerG_emote,
                                                                  player_h_mle_name=playerH_name,
                                                                  player_h_emote=playerH_emote,
                                                                  team_img=self.__get_emote_by_id__(
                                                                      EMOTE_SABRES_NO_BG_ID).url)
        hti.screenshot(html_str=html_string, css_file='..\TeamQuickInfo.css',
                       save_as=f'{get_league_text(self.league)}.png')

        with open(f'{get_league_text(self.league)}.png', 'rb') as f:
            if ctx:
                # noinspection PyTypeChecker
                await ctx.send(file=discord.File(f))
            # noinspection PyTypeChecker
            await self.channel.send(file=discord.File(f))

    async def post_season_stats_html(self,
                                     game_mode: str,
                                     ctx: discord.ext.commands.Context | discord.TextChannel | None = None):
        """ Helper function to post season stats html to the quick info channel of this team (Standard or Doubles, individually)\n
                **param game_mode**: specified game mode that is being posted ('Standard' or 'Doubles')\n
                **`optional`param ctx**: specified context to send information to. If not supplied, the info is posted to the team's quick info channel.\n
                **returns** None\n
                """
        """ Get weekly information and store into a local dict
        """
        await self.update()
        wk = {}
        for i in range(1, 14):
            wk[f'{i}'] = self.__get_weekly_info__(game_mode, f'Match {i}')

        """ Temporary integers to hold info on html image size
            Ideally, this should be placed into the .env file or something similar... Better sizing needs to happen
        """
        width = 615
        height = 750

        """ Create html 2 image object"""
        hti = Html2Image(size=(width, height))

        """ Create a formatted version of the template file
            The dictionary above will fill out this file
        """
        html_string = open(r'team/html/TeamWeeklyStats.html').read().format(league=get_league_text(self.league),
                                                                            mode=game_mode,
                                                                            home_team_wk_1=wk['1']['home_team'],
                                                                            away_team_wk_1=wk['1']['away_team'],
                                                                            home_team_wk_1_clr=wk['1']['home_color'],
                                                                            away_team_wk_1_clr=wk['1']['away_color'],
                                                                            home_team_wk_1_logo=wk['1']['home_url'],
                                                                            away_team_wk_1_logo=wk['1']['away_url'],
                                                                            score_wk_1=wk['1']['score'],
                                                                            home_team_wk_2=wk['2']['home_team'],
                                                                            away_team_wk_2=wk['2']['away_team'],
                                                                            home_team_wk_2_clr=wk['2']['home_color'],
                                                                            away_team_wk_2_clr=wk['2']['away_color'],
                                                                            home_team_wk_2_logo=wk['2']['home_url'],
                                                                            away_team_wk_2_logo=wk['2']['away_url'],
                                                                            score_wk_2=wk['2']['score'],
                                                                            home_team_wk_3=wk['3']['home_team'],
                                                                            away_team_wk_3=wk['3']['away_team'],
                                                                            home_team_wk_3_clr=wk['3']['home_color'],
                                                                            away_team_wk_3_clr=wk['3']['away_color'],
                                                                            home_team_wk_3_logo=wk['3']['home_url'],
                                                                            away_team_wk_3_logo=wk['3']['away_url'],
                                                                            score_wk_3=wk['3']['score'],
                                                                            home_team_wk_4=wk['4']['home_team'],
                                                                            away_team_wk_4=wk['4']['away_team'],
                                                                            home_team_wk_4_clr=wk['4']['home_color'],
                                                                            away_team_wk_4_clr=wk['4']['away_color'],
                                                                            home_team_wk_4_logo=wk['4']['home_url'],
                                                                            away_team_wk_4_logo=wk['4']['away_url'],
                                                                            score_wk_4=wk['4']['score'],
                                                                            home_team_wk_5=wk['5']['home_team'],
                                                                            away_team_wk_5=wk['5']['away_team'],
                                                                            home_team_wk_5_clr=wk['5']['home_color'],
                                                                            away_team_wk_5_clr=wk['5']['away_color'],
                                                                            home_team_wk_5_logo=wk['5']['home_url'],
                                                                            away_team_wk_5_logo=wk['5']['away_url'],
                                                                            score_wk_5=wk['5']['score'],
                                                                            home_team_wk_6=wk['6']['home_team'],
                                                                            away_team_wk_6=wk['6']['away_team'],
                                                                            home_team_wk_6_clr=wk['6']['home_color'],
                                                                            away_team_wk_6_clr=wk['6']['away_color'],
                                                                            home_team_wk_6_logo=wk['6']['home_url'],
                                                                            away_team_wk_6_logo=wk['6']['away_url'],
                                                                            score_wk_6=wk['6']['score'],
                                                                            home_team_wk_7=wk['7']['home_team'],
                                                                            away_team_wk_7=wk['7']['away_team'],
                                                                            home_team_wk_7_clr=wk['7']['home_color'],
                                                                            away_team_wk_7_clr=wk['7']['away_color'],
                                                                            home_team_wk_7_logo=wk['7']['home_url'],
                                                                            away_team_wk_7_logo=wk['7']['away_url'],
                                                                            score_wk_7=wk['7']['score'],
                                                                            home_team_wk_8=wk['8']['home_team'],
                                                                            away_team_wk_8=wk['8']['away_team'],
                                                                            home_team_wk_8_clr=wk['8']['home_color'],
                                                                            away_team_wk_8_clr=wk['8']['away_color'],
                                                                            home_team_wk_8_logo=wk['8']['home_url'],
                                                                            away_team_wk_8_logo=wk['8']['away_url'],
                                                                            score_wk_8=wk['8']['score'],
                                                                            home_team_wk_9=wk['9']['home_team'],
                                                                            away_team_wk_9=wk['9']['away_team'],
                                                                            home_team_wk_9_clr=wk['9']['home_color'],
                                                                            away_team_wk_9_clr=wk['9']['away_color'],
                                                                            home_team_wk_9_logo=wk['9']['home_url'],
                                                                            away_team_wk_9_logo=wk['9']['away_url'],
                                                                            score_wk_9=wk['9']['score'],
                                                                            home_team_wk_10=wk['10']['home_team'],
                                                                            away_team_wk_10=wk['10']['away_team'],
                                                                            home_team_wk_10_clr=wk['10'][
                                                                                'home_color'],
                                                                            away_team_wk_10_clr=wk['10'][
                                                                                'away_color'],
                                                                            home_team_wk_10_logo=wk['10'][
                                                                                'home_url'],
                                                                            away_team_wk_10_logo=wk['10'][
                                                                                'away_url'],
                                                                            score_wk_10=wk['10']['score'],
                                                                            home_team_wk_11=wk['11']['home_team'],
                                                                            away_team_wk_11=wk['11']['away_team'],
                                                                            home_team_wk_11_clr=wk['11'][
                                                                                'home_color'],
                                                                            away_team_wk_11_clr=wk['11'][
                                                                                'away_color'],
                                                                            home_team_wk_11_logo=wk['11'][
                                                                                'home_url'],
                                                                            away_team_wk_11_logo=wk['11'][
                                                                                'away_url'],
                                                                            score_wk_11=wk['11']['score'],
                                                                            home_team_wk_12=wk['12']['home_team'],
                                                                            away_team_wk_12=wk['12']['away_team'],
                                                                            home_team_wk_12_clr=wk['12'][
                                                                                'home_color'],
                                                                            away_team_wk_12_clr=wk['12'][
                                                                                'away_color'],
                                                                            home_team_wk_12_logo=wk['12'][
                                                                                'home_url'],
                                                                            away_team_wk_12_logo=wk['12'][
                                                                                'away_url'],
                                                                            score_wk_12=wk['12']['score'],
                                                                            home_team_wk_13=wk['13']['home_team'],
                                                                            away_team_wk_13=wk['13']['away_team'],
                                                                            home_team_wk_13_clr=wk['13'][
                                                                                'home_color'],
                                                                            away_team_wk_13_clr=wk['13'][
                                                                                'away_color'],
                                                                            home_team_wk_13_logo=wk['13'][
                                                                                'home_url'],
                                                                            away_team_wk_13_logo=wk['13'][
                                                                                'away_url'],
                                                                            score_wk_13=wk['13']['score'],
                                                                            team_imgurl=self.franchise.bot.server_icon)

        hti.screenshot(html_str=html_string, css_file=r'team/html/TeamWeeklyStats.css',
                       save_as=f'{get_league_text(self.league)}weeklystats_{game_mode}.png')

        """ Open the newly created .png file and post it!
        """
        with open(f'{get_league_text(self.league)}weeklystats_{game_mode}.png', 'rb') as f:
            if ctx:
                # noinspection PyTypeChecker
                return await ctx.send(file=discord.File(f))
            # noinspection PyTypeChecker
            await self.channel.send(file=discord.File(f))

    def __process_matches__(self, sprocket_matches: [{}],
                            as_standard: bool) -> None:
        """ Helper function to parse through supplied sprocket matches (Singles or Doubles, individually)\n
        **param sprocket_matches**: dictionary of matches.json from sprocket (usually supplied by sprocket class)\n
        **param as_standard**: bool used to determined mode where **True** is standard mode\n
        **returns** None\n
        For additional information about Sprocket Data Sets and these dictionaries, see:\n
        https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html
        """
        """ Set a string to match based on mode
        """
        mode = "Standard" if as_standard else "Doubles"

        """ Parse matches that match the mode we're in (set by the string above)"""
        for match in [x for x in sprocket_matches if x['game_mode'] == mode]:
            """ Parse wins or losses based on winning team's name
                Also, use the boolean mode to determine which stats to increase
            """
            if match['winning_team'] == self.franchise.franchise_name:
                if as_standard:
                    self.standard_series_wins += 1
                else:
                    self.doubles_series_wins += 1
            else:
                if as_standard:
                    self.standard_series_losses += 1
                else:
                    self.doubles_series_losses += 1

            """ Same as above but in-line
            """
            if as_standard:
                self.standard_wins += match['home_wins'] if self.franchise.franchise_name == match['home'] else match[
                    'away_wins']
                self.standard_losses += match['away_wins'] if self.franchise.franchise_name == match['home'] else match[
                    'home_wins']
            else:
                self.doubles_wins += match['home_wins'] if self.franchise.franchise_name == match['home'] else match[
                    'away_wins']
                self.doubles_losses += match['away_wins'] if self.franchise.franchise_name == match['home'] else match[
                    'home_wins']

    def __reset_match_data__(self) -> None:
        """ Helper method to reset all match datas to 0\n
            This method is only intended to be used internally by this class\n
            To properly reset match data externally, run the **update** method
        """
        self.standard_series_wins = 0
        self.standard_series_losses = 0
        self.standard_wins = 0
        self.standard_losses = 0
        self.doubles_series_wins = 0
        self.doubles_series_losses = 0
        self.doubles_wins = 0
        self.doubles_losses = 0

    async def update_from_sprocket_data(self) -> None:
        """ Update this team's information from supplied sprocket data\n
                **param sprocket_data**: dictionary of .json data from sprocket (usually supplied by sprocket class)\n
                **returns** None\n
                For additional information about Sprocket Data Sets and these dictionaries, see:\n
                https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html
                """
        """ Begin by clearing out match data
         """
        self.__reset_match_data__()
        sprocket_data = self.franchise.bot.sprocket.data

        """ validate data
        """
        if not sprocket_data:
            return
        if not sprocket_data['sprocket_matches']:
            return
        if not sprocket_data['sprocket_match_groups']:
            return

        """ Get valid, played matches from supplied sprocket data
        """
        self.get_played_matches(sprocket_matches=sprocket_data['sprocket_matches'],
                                sprocket_match_groups=sprocket_data['sprocket_match_groups'])

        """ If no played matches were found, do not continue the process
        """
        if not self.played_matches:
            return await err(f'Could not find valid, played matches for\n'
                             f'team {self.franchise.franchise_name}\n'
                             f'league {self.league}\n')

        """ Process standard series matches
        """
        self.__process_matches__(sprocket_matches=self.played_matches,
                                 as_standard=True)

        """ Process doubles series matches
                """
        self.__process_matches__(sprocket_matches=self.played_matches,
                                 as_standard=False)

    def add_member(self,
                   new_member: Member) -> bool:
        """ Add a MLE member to this team's roster\n
                        **param member**: MLE Member to be added to this roster\n
                        **returns** Success status of add\n
                        """
        """ Validate the member's league is the same as this teams'
        """
        if new_member.league != self.league:
            return False
        """ Validate that the member isn't already a part of our team
        """
        if new_member in self.players:
            return False
        """ Add the member
        """
        self.players.append(new_member)
        new_member.update(self.franchise.bot.sprocket.data)
        return True

    def build(self):
        self._sprocket_players = [x for x in self.franchise.sprocket_players if x['skill_group'] == self.league_name]
        self._sprocket_members = []
        for _player in self._sprocket_players:
            _mem = next((x for x in self.franchise.sprocket_members if x['member_id'] == _player['member_id']), None)
            if _mem:
                self._sprocket_members.append(_mem)
                _guild_member = next((x for x in self.franchise.guild.members if x.id == int(_mem['discord_id'])), None)
                if _guild_member:
                    self.add_member(Member(_guild_member,
                                           self.league))

    async def build_quick_info_channel(self,
                                       sprocket_data: {}) -> None:
        """ Build quick info channel for this MLE team\n
            Note: This method will return if no channel exists.\n
            This function will clear the Quick Info channel messages (up to 100) and post various pieces of quick info\n
            **param sprocket_data**: dictionary of .json data from sprocket (usually supplied by sprocket class)\n
            **returns**: None\n
                """
        """ If no channel exists, immediately return
                """
        if not self.channel:
            return
        """ Clear out channel messages as much as we can
                """
        await channels.clear_channel_messages(self.channel, 100)

        """ Send notification that an update is running
                """
        await err(f'Running new quick info channel information.\n'
                  f'{self.franchise_name} - {self.league}')

        """ Send the team quick info html doc to the team's quick info channel
                """
        await self.__post_quick_info_html__()

        """ Use helper function to send html doc of Standard matches to quick info channel 
                """
        await self.___post_season_stats_html__('Standard')

        """ Use helper function to send html doc of Doubles matches to quick info channel 
                """
        await self.___post_season_stats_html__('Doubles')

    def get_played_matches(self, sprocket_matches: {}, sprocket_match_groups: {}) -> [{}] or None:
        """ Get played matches from sprocket data\n
        **param sprocket_matches**: dictionary of matches.json from sprocket (usually supplied by sprocket class)\n
        **param sprocket_match_groups**: dictionary of match_groups.json from sprocket (usually supplied by sprocket class)\n
        **returns** dictionary of valid, played matches from the current MLE season\n
        For additional information about Sprocket Data Sets and these dictionaries, see:\n
        https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html
        """

        """ Get games that include this team as either home or away
            param x: rocket league series played in MLE
        """
        matches = [x for x in sprocket_matches if
                   ((x['home'] == self.franchise.franchise_name) | (x['away'] == self.franchise.franchise_name)) and
                   x['league'] == get_league_text(self.league)]

        """ Get valid match groups that occurred this current season
            param x: match group hosted by sprocket that includes season data
        """
        match_groups = [x for x in sprocket_match_groups if x['parent_group_title'] == os.getenv('SEASON')]

        """ Compare the two previous search results to come up with a final list of valid, played matches this season 
            param x: rocket league series played in MLE
            param y: match group of series' played in MLE
        """
        valid_season_matches = [x for x in matches for y in match_groups if
                                x['match_group_id'] == y['match_group_id']]

        """ Return only games that have been played
            Games with the winning team marked as below have not been played, so these should not be included
            param x: matches from this season that include our team
            """
        self.played_matches = [x for x in valid_season_matches if
                               (x['winning_team'] != "Not Played / Data Unavailable")]
        return self.played_matches

    async def get_updated_players(self) -> [Member]:
        for player in self.players:
            player.update(self.franchise.bot.sprocket.data)
        return self.players

    def remove_member(self, _member: Member) -> bool:
        if _member in self.players:
            self.players.remove(_member)
            return True
        return False

    async def update(self):
        """ Update MLE Team from supplied sprocket data\n
            This method is a callback for the sprocket periodic data task\n
            This method will **rebuild the team's quick info channel** (if it has one)
            **param sprocket_data**: dictionary provided by Sprocket class of all sprocket public datasets\n
            **returns**: None\n
            For additional information about Sprocket Data Sets and these dictionaries, see:\n
            https://f004.backblazeb2.com/file/sprocket-artifacts/public/pages/index.html
            """
        """ Update self with the newly provided sprocket data
        """
        await self.update_from_sprocket_data()

        """ Update players with the new sprocket data
        """
        for player in self.players:
            await player.update(self.sprocket_data)

        """ Finally, after everything has been updated, build the quick info channel
        """
        await self.build_quick_info_channel(self.sprocket_data)


def get_league_text(league: LeagueEnum) -> str | None:
    """ Get text representation of League enumeration """

    match league:
        case LeagueEnum.Premier_League:
            return "Premier League"
        case LeagueEnum.Master_League:
            return "Master League"
        case LeagueEnum.Champion_League:
            return "Champion League"
        case LeagueEnum.Academy_League:
            return "Academy League"
        case LeagueEnum.Foundation_League:
            return "Foundation League"


def get_league_text_short(league) -> str | None:
    """ Get shorthand string representation of League enumeration """

    match league:
        case LeagueEnum.Premier_League:
            return "PL"
        case LeagueEnum.Master_League:
            return "ML"
        case LeagueEnum.Champion_League:
            return "CL"
        case LeagueEnum.Academy_League:
            return "AL"
        case LeagueEnum.Foundation_League:
            return "FL"


def get_defined_team_players(_team: {},
                             _sprocket_data: {}):
    if not _sprocket_data or not _team:
        return None
    _all = [x for x in _sprocket_data['sprocket_players'] if x['franchise'] == _team['name']]
    return {
        'all': _all,
        'fm': next((x for x in _all if x['Franchise Staff Position'] == 'Franchise Manager'), None),
        'gms': [x for x in _all if x['Franchise Staff Position'] == 'General Manager'],
        'agms': [x for x in _all if x['Franchise Staff Position'] == 'Assistant General Manager'],
        'captains': [x for x in _all if x['Franchise Staff Position'] == 'Captain'],
        'pr_supports': [x for x in _all if x['Franchise Staff Position'] == 'PR Support'],

        'pl_players': [x for x in _all if x['skill_group'] == 'Premier League' and x['slot'] != 'NONE'],
        'ml_players': [x for x in _all if x['skill_group'] == 'Master League' and x['slot'] != 'NONE'],
        'cl_players': [x for x in _all if x['skill_group'] == 'Champion League' and x['slot'] != 'NONE'],
        'al_players': [x for x in _all if x['skill_group'] == 'Academy League' and x['slot'] != 'NONE'],
        'fl_players': [x for x in _all if x['skill_group'] == 'Foundation League' and x['slot'] != 'NONE'],
    }


def get_mle_franchise_embed(_team: {}) -> discord.Embed:
    embed = (discord.Embed(color=discord.Color.from_str(_team['primary_color']),
                           title=f"{_team['name']} Roster")
             .set_footer(text=f"Generated: {datetime.datetime.now().strftime('%c')}"))
    embed.set_thumbnail(url=_team['logo_img_link'])
    return embed
