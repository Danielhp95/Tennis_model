import os, sys

daos_path = os.path.abspath(os.path.join(__file__, '..','..'))
sys.path.append(daos_path)
from daos import bettingDao as betdao
from daos import tennisAtpDao as atpdao
from daos.decorators import atp_to_betting as dec

class BettingRun(object):

    '''
        Initial money
        ROI
        MODEL
        BETTING STRATEGY
        DATA_POINTS
        -Dirty run 
            -Can look into the future
            -Can spend money and go negative

        Will need to give data as input to model. In common opponent this can be done by modifying the 'common_opponents' function
        to take in a data frame as a parameter.

        All data can be calculated using the decorator. Then we can just use some of those indexes to do the betting run. This saves us the effort
        of pre computing the data to fit into the model with every iteration. The match to calculate is will be the index at hand. The data to fit 
        into the model will be anything index lower than the current one. Look into df.re_index(drop=True)
    '''

    def __init__(self, initial_money=0, model=None,
                 earliest_year=None, latest_year=None, courts=None,
                 tournaments=None, players=None, rounds=None, best_of=None,
                 rank_position=None, rank_points=None):
        assert initial_money > 0, '{initial money} must be positive'
        #assert model is not None, 'There must be an input {model} to calculate the match odds' TODO: remove assertions for now
        #assert getattr(model, 'TODO', None) is not None, '{model} must implement TODO'
        assert earliest_year is not None, '{earliest_year} must be set'
        assert earliest_year >= 2006, '{earliest_year} must be greater or equal than 2006 (oldest recorded data)'
        assert latest_year >= earliest_year, '{latest_year} must be greater or equal thatn {earliest_year}'
        assert latest_year <= betdao.CURRENT_YEAR, '{latest_year} must be less or equal than ' + betdao.CURRENT_YEAR
        
        atp_matches, wta_matches = self.gather_data(earliest_year, latest_year)

        atp_matches, wta_matches = self.apply_filters(courts, tournaments,
                                                      players, rounds,
                                                      best_of, rank_position,
                                                      rank_points)
        print(atp_matches)


        # Now I only need to find first to compute (last will be the last in the list)
            # Possibilities: - Load until {earliest_year}, get last index and load until {latest_year}
            # Possibilities: - DO IT ALL AT ONCE


    def gather_data(self, earliest_year, latest_year):
        atp_df, wta_df = atpdao.read_by_date(earliest_year, latest=latest_year)
        atp_bet_df, wta_bet_df = atpdao.read_by_date(earliest_year, latest=latest_year)

        atp_matches = dec.join_atp_and_bet_tables(atp=atp_df, bet=atp_bet_df)
        wta_matches = dec.join_atp_and_bet_tables(atp=wta_df, bet=wta_bet_df)
        return atp_matches, wta_matches

    def apply_filters(self, courts, tournaments, players, rounds,
                      best_of, rank_position, rank_points):
        # Filter by all input paratemers if present
        if tournaments is not None:
            atp_matches = tennisAtpDao.filter_by_tournament(atp_matches, tournaments)
            wta_matches = tennisAtpDao.filter_by_tournament(wta_matches, tournaments)
        if players is not None:
            atp_matches = tennisAtpDao.filter_by_players(atp_matches, players)
            wta_matches = tennisAtpDao.filter_by_players(wta_matches, players)
        if rounds is not None:
            atp_matches = bettingDao.filter_by_round(atp_matches, rounds)
            wta_matches = bettingDao.filter_by_round(wta_matches, rounds)
        if best_of is not None:
            atp_matches = tennisAtpDao.filter_by_best_of(atp_matches, best_of)
            wta_matches = tennisAtpDao.filter_by_best_of(wta_matches, best_of)
        if rank_position is not None:
            atp_matches = bettingDao.filter_by_rank_position(atp_matches, rank_position)
            wta_matches = bettingDao.filter_by_rank_position(wta_matches, rank_position)
        if rank_points is not None:
            atp_matches = bettingDao.filter_by_rank_points(atp_matches, rank_points)
            wta_matches = bettingDao.filter_by_rank_points(wta_matches, rank_points)
        return atp_matches, wta_matches

    def data_to_list(df):
        return df.to_dict('records')
