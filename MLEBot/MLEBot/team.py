""" Minor League E-Sports Team
# Author: irox_rl
# Purpose: General Functions of a League Team
# Version 3.00.01
"""
import os
import channels
import discord
from discord.ext import commands
from err import err
from html2image import Html2Image
import member
import enums

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
                 league: enums.LeagueEnum) -> None:
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
        self.players: [member.Member] = []
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

    @property
    def league_name(self) -> str:
        return self.league.name

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
        playerA: member.Member | None = next((x for x in self.players if x.role == 'PLAYERA'), None)
        playerB: member.Member | None = next((x for x in self.players if x.role == 'PLAYERB'), None)
        playerC: member.Member | None = next((x for x in self.players if x.role == 'PLAYERC'), None)
        playerD: member.Member | None = next((x for x in self.players if x.role == 'PLAYERD'), None)
        playerE: member.Member | None = next((x for x in self.players if x.role == 'PLAYERE'), None)
        playerF: member.Member | None = next((x for x in self.players if x.role == 'PLAYERF'), None)
        playerG: member.Member | None = next((x for x in self.players if x.role == 'PLAYERG'), None)
        playerH: member.Member | None = next((x for x in self.players if x.role == 'PLAYERH'), None)
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
                                                                               team_img=self.franchise.bot.get_emoji(self.franchise.bot.server_icon).url)

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
                   new_member: member.Member) -> bool:
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
        return True

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

    def compress(self):
        return {
            'sprocket_players': [x.compress() for x in self.players],
            'message_id': self.message_id,
            'standard_series_wins': self.standard_series_wins,
            'standard_series_losses': self.standard_series_losses,
            'standard_wins': self.standard_wins,
            'standard_losses': self.standard_losses,
            'doubles_series_wins': self.doubles_series_wins,
            'doubles_series_losses': self.doubles_series_losses,
            'doubles_wins': self.doubles_wins,
            'doubles_losses': self.doubles_losses,
        }

    async def decompress(self, pickle_data, guild: discord.Guild, channel: discord.TextChannel):
        self.guild = guild
        self.channel = channel
        for data in pickle_data['sprocket_players']:
            self.add_member(member.Member.from_pickle(self.guild,
                                                      data))
        if pickle_data['message_id']:
            self.message_id = pickle_data['message_id']
            self.message = await channels.get_channel_message_by_id(self.channel, self.message_id.__str__())
        try:
            self.standard_series_wins = pickle_data['standard_series_wins']
            self.standard_series_losses = pickle_data['standard_series_losses']
            self.standard_wins = pickle_data['standard_wins']
            self.standard_losses = pickle_data['standard_losses']
            self.doubles_series_wins = pickle_data['doubles_series_wins']
            self.doubles_series_losses = pickle_data['doubles_series_losses']
            self.doubles_wins = pickle_data['doubles_wins']
            self.doubles_losses = pickle_data['doubles_losses']
        except KeyError:
            pass

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

    def remove_member(self, _member: member.Member) -> bool:
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


def get_league_role(_member: discord.Member) -> enums.LeagueEnum | None:
    """ Returns league enumeration if user has associated role
        else returns None """

    for role in _member.roles:
        match role.name:
            case 'Premier League':
                return enums.LeagueEnum.Premier_League
            case 'Master League':
                return enums.LeagueEnum.Master_League
            case 'Champion League':
                return enums.LeagueEnum.Champion_League
            case 'Academy League':
                return enums.LeagueEnum.Academy_League
            case 'Foundation League':
                return enums.LeagueEnum.Foundation_League


def get_league_text(league: enums.LeagueEnum) -> str | None:
    """ Get text representation of League enumeration """

    match league:
        case enums.LeagueEnum.Premier_League:
            return "Premier League"
        case enums.LeagueEnum.Master_League:
            return "Master League"
        case enums.LeagueEnum.Champion_League:
            return "Champion League"
        case enums.LeagueEnum.Academy_League:
            return "Academy League"
        case enums.LeagueEnum.Foundation_League:
            return "Foundation League"


def get_league_text_short(league) -> str | None:
    """ Get shorthand string representation of League enumeration """

    match league:
        case enums.LeagueEnum.Premier_League:
            return "PL"
        case enums.LeagueEnum.Master_League:
            return "ML"
        case enums.LeagueEnum.Champion_League:
            return "CL"
        case enums.LeagueEnum.Academy_League:
            return "AL"
        case enums.LeagueEnum.Foundation_League:
            return "FL"
