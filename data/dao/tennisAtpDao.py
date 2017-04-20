from pandas import read_csv
import pandas as pd

DATA_DIR = r'/home/dh1213/tennis_model/data/tennis_atp/'
MATCHES = 'atp_matches_'
CURRENT_YEAR = 2017 # Change once a year!

def common_opponents(player_a, player_b, from_year=CURRENT_YEAR):
    match_info = concatenate_match_info_since(from_year)

    # Opponents are filtered to remove rows with NaN values in serve related areas
    player_a_opponents = find_opponents_for_player(player_a, match_info)
    player_b_opponents = find_opponents_for_player(player_b, match_info)

    # Compute intersection of opponents and remove both players from result
    # to avoid cases in which players have faced each other. TODO: ask Will about this
    com_opponents = (player_a_opponents & player_b_opponents) - set([player_a, player_b])


    # Find common opponents
    com_opponents_info = match_info[((match_info.winner_name == player_a) & (match_info.loser_name.isin(com_opponents))) |
                                    ((match_info.loser_name == player_a) & (match_info.winner_name.isin(com_opponents))) |
                                    ((match_info.winner_name == player_b) & (match_info.loser_name.isin(com_opponents))) |
                                    ((match_info.loser_name == player_b) & (match_info.winner_name.isin(com_opponents)))]

    # Second NaN filtering
    com_opponents_info = com_opponents_info[(pd.notnull(com_opponents_info.w_1stWon)) &
                          (pd.notnull(com_opponents_info.w_2ndWon)) &
                          (pd.notnull(com_opponents_info.w_svpt)) &
                          (pd.notnull(com_opponents_info.l_1stWon)) &
                          (pd.notnull(com_opponents_info.l_2ndWon)) &
                          (pd.notnull(com_opponents_info.l_svpt))]

    return com_opponents, com_opponents_info

def concatenate_match_info_since(from_year):
    all_frames = map(lambda x: pd.read_csv(x), [DATA_DIR + MATCHES + str(year) + '.csv' for year in range(CURRENT_YEAR, from_year -1, -1)])
    years = [str(year) for year in range(CURRENT_YEAR, from_year -1, -1)]
    print(years)
    return pd.concat(all_frames, keys=years)
        

'''
 Finds all matches in which PLAYER has participated.
 Creates a set containing all of those players, and removes the player himself from it
'''
def find_opponents_for_player(player, match_info):
    opponents = match_info[(match_info.winner_name == player) |
                             (match_info.loser_name == player)]

    opponents = opponents[(pd.notnull(match_info.w_1stWon)) &
                          (pd.notnull(match_info.w_2ndWon)) &
                          (pd.notnull(match_info.w_svpt)) &
                          (pd.notnull(match_info.l_1stWon)) &
                          (pd.notnull(match_info.l_2ndWon)) &
                          (pd.notnull(match_info.l_svpt))]

    return (set(opponents.winner_name) | set(opponents.loser_name)) - set(player)

def common_opponent_print_filter(data_frame):
    return data_frame.filter(items=['winner_name','loser_name',
                                     'w_svpt', 'w_1stWon', 'w_2ndWon',
                                     'l_svpt', 'l_1stWon', 'l_2ndWon'])
