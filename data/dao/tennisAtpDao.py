from pandas import read_csv
import pandas as pd

DATA_DIR    = r'/home/dh1213/tennis_model/data/tennis_atp/'
MATCH_FILES = 'atp_matches_' # File name follow pattern -> atp_matches_{year}.csv 
EXTENSION   = '.csv'
CURRENT_YEAR = 2017 # Change once a year!

def common_opponents(player_a, player_b, courts=["Hard","Clay","Grass","Carpet"],
                     latest_year=CURRENT_YEAR, earliest_year=CURRENT_YEAR):

    match_info = load_by_year(DATA_DIR + MATCH_FILES, latest_year, earliest_year)

    # Surface filtering
    com_opponents_info = filter_by_court(match_info, courts)

    # Opponents are filtered to remove rows with NaN values in serve related areas
    player_a_opponents = find_opponents_for_player(player_a, match_info)
    player_b_opponents = find_opponents_for_player(player_b, match_info)

    # Compute intersection of opponents and remove both players from result
    # to avoid cases in which players have faced each other. TODO: ask Will about this
    com_opponents = (player_a_opponents & player_b_opponents) - set([player_a, player_b])

    # Find common opponents
    com_opponents_info = filter_by_common_opponent(com_opponents_info, player_a, player_b, com_opponents)

    # Second NaN filtering
    com_opponents_info = filter_nan(com_opponents_info)

    return com_opponents, com_opponents_info

'''
    Years decrement in loops because most recent data is the most valuable
    for any model.
'''
def load_by_year(directory, latest_year, earliest_year=None, df=None, keys=[]):
    if earliest_year == None:
        earliest_year = latest_year
    range_of_years = [str(year) for year in range(latest_year, earliest_year -1, -1)]
    all_frames_lst = map(lambda x: pd.read_csv(x,skipinitialspace=True), 
                         [directory + year + EXTENSION for year in range_of_years])
   
    all_frames = pd.concat(all_frames_lst, keys=range_of_years)
    if df !=None:
        all_frames = pd.concat(df, keys=keys)
    return all_frames
   
# TODO: consider court where there is no surface data
def filter_by_court(df, courts):
    return df[df.surface.isin(courts)]

def filter_by_common_opponent(df, player_a, player_b, com_opponents):
    return  df[((df.winner_name == player_a) & (df.loser_name.isin(com_opponents))) |
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
