import os
import pandas as pd
from pandas import read_csv

MEN_DATA_DIR     = os.path.abspath(os.path.join(__file__, '..','..', '..','data','tennis_atp')) + '/atp_matches_'
WOMEN_DATA_DIR   = os.path.abspath(os.path.join(__file__, '..','..', '..','data','tennis_wta')) + '/wta_matches_'
EXTENSION    = '.csv'
CURRENT_YEAR = 2017 # Change once a year!

def common_opponents(player_a, player_b, courts=["Hard","Clay","Grass","Carpet"],
                     earliest=CURRENT_YEAR, latest=CURRENT_YEAR):

    atp_match_info, wta_match_info = read_by_date(earliest, latest=latest)

    match_info = atp_match_info # TODO: have league as an input

    # Surface filtering
    com_opponents_info = filter_by_court(match_info, courts)

    # Opponents are filtered to remove rows with NaN values in serve related areas
    player_a_opponents = find_opponents_for_player(player_a, match_info)
    player_b_opponents = find_opponents_for_player(player_b, match_info)

    # Compute intersection of opponents and remove both players from result
    # to avoid cases in which players have faced each other.
    com_opponents = (player_a_opponents & player_b_opponents) - set([player_a, player_b])

    # Find common opponents
    com_opponents_info = filter_by_common_opponent(com_opponents_info, player_a, player_b, com_opponents)

    # Second NaN filtering
    com_opponents_info = filter_nan(com_opponents_info)

    return com_opponents, com_opponents_info

def read_by_date(earliest, latest=CURRENT_YEAR, df=None):
    range_of_years = [str(year) for year in range(latest, earliest -1, -1)]
    atp_frames     = map(lambda x: pd.read_csv(x,skipinitialspace=True), 
                         [MEN_DATA_DIR + year + EXTENSION for year in range_of_years])
    wta_frames     = map(lambda x: pd.read_csv(x,skipinitialspace=True), 
                         [WOMEN_DATA_DIR + year + EXTENSION for year in range_of_years])
   
    atp_all_frames = pd.concat(atp_frames, keys=range_of_years)
    wta_all_frames = pd.concat(wta_frames, keys=range_of_years)
    return atp_all_frames, wta_all_frames
   
# TODO: consider court where there is no surface data
def filter_by_court(df, courts):
    return df[df.surface.isin(courts)]

def filter_by_player(df, player):
    if isinstance(player, list):
        return df[(df.winner_name.isin(player)) | (df.loser_name.isin(player))]
    return df[(df.winner_name == player) | (df.loser_name == player)]

def filter_by_common_opponent(df, player_a, player_b, com_opponents):
    return df[((df.winner_name == player_a) & (df.loser_name.isin(com_opponents))) |
               ((df.loser_name == player_a) & (df.winner_name.isin(com_opponents))) |
               ((df.winner_name == player_b) & (df.loser_name.isin(com_opponents))) |
               ((df.loser_name == player_b) & (df.winner_name.isin(com_opponents)))]

'''
    Finds all matches in which PLAYER has participated.
    Creates a set containing all of those players, and 
    removes the player himself from the data frame:
'''
def find_opponents_for_player(player, match_info):
    opponents = match_info[(match_info.winner_name == player) |
                             (match_info.loser_name == player)]
    
    opponents = filter_nan(opponents)

    return (set(opponents.winner_name) | set(opponents.loser_name)) - set(player)

def filter_nan(df):
    return df[(pd.notnull(df.w_1stWon)) &
              (pd.notnull(df.w_2ndWon)) &
              (pd.notnull(df.w_svpt)) &
              (pd.notnull(df.l_1stWon)) &
              (pd.notnull(df.l_2ndWon)) &
              (pd.notnull(df.l_svpt))]

'''
    For debugging purposes
'''
def common_opponent_print_filter(data_frame):
    return data_frame.filter(items=['winner_name','loser_name',
                                     'w_svpt', 'w_1stWon', 'w_2ndWon',
                                     'l_svpt', 'l_1stWon', 'l_2ndWon'])
