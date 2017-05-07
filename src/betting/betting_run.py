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
                 earliest_year=None, latest_year=None, courts=None
                 tournaments=None, players=None, rounds=None, best_of=None
                 rank_position=None, rank_points=None):
        assert initial_money > 0, '{initial money} must be positive'
        assert model is not None, 'There must be an input {model} to calculate the match odds'
        assert getattr(model, 'TODO', None) is not None, '{model} must implement TODO'
        assert earliest_year is not None, '{earliest_year} must be set'
        assert earliest_year >= 2006, '{earliest_year} must be greater or equal than 2006 (oldest recorded data)'
        assert latest_year >= earliest_year, '{latest_year} must be greater or equal thatn {earliest_year}'
        assert latest_year <= betdao.CURRENT_YEAR, '{latest_year} must be less or equal than ' + betdao.CURRENT_YEAR
        
        

    def data_to_list(df):
        return df.to_dict('records')
