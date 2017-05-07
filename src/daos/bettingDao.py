import os
import pandas as pd
from pandas import read_excel

# women matches files are finished by a 'w'
DATA_DIR     = os.path.abspath(os.path.join(__file__, '..', '..', '..','data','betting')) + '/'
CURRENT_YEAR = 2017

def read_by_date(earliest, latest=CURRENT_YEAR, ignore_wtp=False):
    range_of_years = [str(year) for year in range(latest, earliest -1, -1)]
    all_frames_lst = map(lambda x: read_excel(x), [DATA_DIR + year for year in range_of_years])

    wtp_all_frames_lst, wtp_df = None, None
    if not ignore_wtp:
        wtp_all_frames_lst = map(lambda x: read_excel(x), [DATA_DIR + year + 'w' for year in range_of_years])
        wtp_all_frames_lst = filter(lambda x: x is not None, wtp_all_frames_lst) # Some years lack women's records
        if len(wtp_all_frames_lst) > 0:
            wtp_df = pd.concat(wtp_all_frames_lst, keys=range_of_years)

    return pd.concat(all_frames_lst, keys=range_of_years), wtp_df

def filter_by_round(df, rounds):
    assert_value_is_within(rounds, ['1st Round', '2nd Round', 'Quarterfinals', 'Semifinals', 'The Final'], "Rounds")
    return df[df.Round.isin(rounds)]

def filter_by_surface(df, surfaces):
    assert_value_is_within(surfaces, ['Clay', 'Carpet', 'Hard', 'Grass'], "Surfaces")
    return df[df.Surface.isin(surfaces)]

def filter_by_best_of(df, best_of):
    df.columns = df.columns.str.replace('\s+', '_') # removes space in Best of Column
    assert_value_is_within([best_of], [3,5], "Best of")
    return df[df.Best_of == best_of]

# TODO: write tests for this function
def filter_by_player(df, player):
    if isinstance(player, list):
        return df[(df.Winner.isin(player)) | (df.Loser.isin(player))]
    return df[(df.Winner == player) | (df.Loser == player)]

def filter_by_tournament(df, tournaments):
    assert_value_is_within(tournaments, df.Tournament.unique(), "Tournaments")
    return df[df.Tournament.isin(tournaments)]

def filter_by_rank_position(df, minimun, maximum=1):
    assert minimun > 0, "Position mas be greater than 0" 
    return df[((df.WRank >= minimun) & (df.WRank <= maximum)) |
              ((df.LRank >= minimun) & (df.LRank <= maximum))]

def filter_by_rank_points(df, minimun, maximum=1):
    assert minimun > 0, "Position mas be greater than 0" 
    return df[((df.WPts >= minimun) & (df.WPts <= maximum)) |
              ((df.LPts >= minimun) & (df.LPts <= maximum))]
# Utils #
def assert_value_is_within(values, possible_values, value_name):
    for v in possible_values:
        assert v in possible_values , value_name + " must be within: " + str(possible_surfaces)

def read_excel(file_path):
    if os.path.isfile(file_path + '.xls'):
        return pd.read_excel(file_path + '.xls')
    elif os.path.isfile(file_path + '.xlsx'):
        return pd.read_excel(file_path + '.xlsx')
    else:
        print("File does not exist " + file_path)
