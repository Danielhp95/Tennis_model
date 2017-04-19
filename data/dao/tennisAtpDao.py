from pandas import read_csv
import pandas as pd



DATA_DIR = r'/home/dh1213/tennis_model/data/tennis_atp/'
MATCHES = 'atp_matches_'

# TODO: figure out how to parameterize how many years will be taken into account
# Return type is a set
def common_opponents(player_a, player_b):
    loc        = DATA_DIR + MATCHES + '2016.csv'
    match_info = pd.read_csv(loc)

    player_a_opponents = find_opponents_for_player(player_a, match_info)
    player_b_opponents = find_opponents_for_player(player_b, match_info)

    # Compute intersection of opponents and remove both players from result
    # to avoid cases in which players have faced each other. TODO: ask Will about this
    com_opponents = (player_a_opponents & player_b_opponents) - set([player_a, player_b])

    return com_opponents
    # TODO: ponder whether this can be improved
    
    #com_opponents_info = match_info[((match_info.winner_name == player_a) & (match_info.loser_name in common_opponents))]

           #                        ((match_info.loser_name == player_a) & (match_info.winner_name in common_opponents)) |
           #                        ((match_info.winner_name == player_b) & (match_info.loser_name in common_opponents)) |
           #                        ((match_info.loser_name == player_b) & (match_info.winner_name in common_opponents))]
    print(com_opponents_info)



'''
 Finds all matches in which PLAYER has participated.
 Creates a set containing all of those players, and removes the player himself from it
'''
def find_opponents_for_player(player, match_info):
    opponents = match_info[(match_info.winner_name == player) |
                             (match_info.loser_name == player)]
    return (set(opponents.winner_name) | set(opponents.loser_name)) - set(player)

def common_opponent_print_filter(data_frame):
    return data_frame.filter(items=['winner_name','loser_name',
                                     'w_svpt', 'w_1stWon', 'w_2ndWon',
                                     'l_svpt', 'l_1stWon', 'l_2ndWon'])

print(common_opponents('Roger Federer', 'Milos Raonic'))
