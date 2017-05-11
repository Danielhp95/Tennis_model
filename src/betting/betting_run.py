from __future__ import division
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
                 rank_position=None, rank_points=None, 
                 strategy=None):
        assert initial_money > 0, '{initial money} must be positive'
        assert model is not None, 'There must be an input {model} to calculate the match odds' 
        assert getattr(model, 'calculate_odds', None) is not None, '{model} must implement calculate_odds function'
        assert earliest_year is not None, '{earliest_year} must be set'
        assert earliest_year >= 2006, '{earliest_year} must be greater or equal than 2006 (oldest recorded data)'
        assert latest_year >= earliest_year, '{latest_year} must be greater or equal thatn {earliest_year}'
        assert latest_year <= betdao.CURRENT_YEAR, '{latest_year} must be less or equal than ' + betdao.CURRENT_YEAR
        assert getattr(strategy, 'strategy', None) is not None, '{strategy} must implement stragegy function'

        self.total_bets    = 0
        self.initial_money = initial_money
        self.atp_matches, self.wta_matches = self.gather_data(earliest_year, latest_year)
        self.atp_bet, self.wta_bet   = self.apply_filters(self.atp_matches, self.wta_matches, courts, tournaments,
                                                      players, rounds,
                                                      best_of, rank_position,
                                                      rank_points)

        self.model    = model
        self.strategy = strategy
        self.initialize_statistics()
        


    def gather_data(self, earliest_year, latest_year):
        return dec.read_by_date(earliest_year, latest_year)

    def apply_filters(self, atp_matches, wta_matches,
                      courts, tournaments, players, rounds,
                      best_of, rank_position, rank_points):
        '''
         Filter by all input paratemers if present
        '''
        filter_atp = atp_matches.copy()
        filter_wta = wta_matches.copy()
        if tournaments is not None:
            filter_atp = betdao.filter_by_tournament(filter_atp, list(tournaments))
            filter_wta = betdao.filter_by_tournament(filter_wta, list(tournaments))
        if players is not None:
            filter_atp = atpdao.filter_by_player(filter_atp, list(players))
            filter_wta = atpdao.filter_by_player(filter_wta, list(players))
        if rounds is not None:
            filter_atp = betdao.filter_by_round(filter_atp, list(rounds))
            filter_wta = betdao.filter_by_round(filter_wta, list(rounds))
        if best_of is not None:
            filter_atp = betdao.filter_by_best_of(filter_atp, best_of)
            filter_wta = betdao.filter_by_best_of(filter_wta, best_of)
        if rank_position is not None:
            filter_atp = betdao.filter_by_rank_position(filter_atp, rank_position)
            filter_wta = betdao.filter_by_rank_position(filter_wta, rank_position)
        if rank_points is not None:
            filter_atp = betdao.filter_by_rank_points(filter_atp, rank_points)
            filter_wta = betdao.filter_by_rank_points(filter_wta, rank_points)
        return filter_atp, filter_wta


    #TODO: abstract this to work on any data, not only atp
    def betting_run(self):
        '''
        TODO: think of the possibility of making this a super class so that
             other implementations of betting_run can be applied
        '''
        # df.sort(['Date'], ascending = 1).reset_index(drop=True)
        ascending_data = self.atp_matches
        filtered_data  = self.atp_bet.sort(['Date'],ascending=1)

        # Betting run for ATP league
        run_money = self.initial_money
        for i, match in filtered_data.iterrows():
            print(match['winner_name'] + ' vs ' + match['loser_name'] + str(match['tourney_date']))

            matches_up_to_date = self.atp_matches[self.atp_matches.Date <= match['Date']]

            # Relevant stats for model and strategy
            winner_average_odds = match['B365W']
            loser_average_odds  = match['B365L']
            player_a            = match['winner_name']
            player_b            = match['loser_name']

            # Model calculations
            model_odds_a = self.model.calculate_odds(player_a, player_b,
                                                     matches_up_to_date)
            model_odds_b = 1.0/model_odds_a

            # Strategies calculations
            # choices must be 'a' or 'b'
            match_bet, choice = self.strategy.strategy(model_odds_a, model_odds_b,
                                   winner_average_odds, loser_average_odds, match) 

            # Calculate outcomes
            positive_outcome = choice == 'a'
            earnings = (match_bet*winner_average_odds - match_bet) if positive_outcome else -match_bet

            # Update statistics
            self.update_match_statistics(run_money, earnings, match)
            run_money += earnings
            if run_money <= 0:
                print('Betting run finishes due to lack of funds')
                break
        
        print("End of betting run")
        return

    def initialize_statistics(self):
        self.statistics = {}
        self.statistics['roi'] = []

    def calculate_ROI(self, current_money, match):
        return (current_money - self.initial_money) / self.initial_money

    def match_betting_odds(self, match):
        winner_betting_odds = []
        loser_betting_odds  = []
        self.safe_append(winner_betting_odds, match, 'B365W')
        self.safe_append(winner_betting_odds, match, 'B&WW')
        self.safe_append(winner_betting_odds, match, 'CBW')
        self.safe_append(winner_betting_odds, match, 'EXW')
        self.safe_append(winner_betting_odds, match, 'LBW')
        self.safe_append(winner_betting_odds, match, 'GBW')
        self.safe_append(winner_betting_odds, match, 'IWW')
        self.safe_append(winner_betting_odds, match, 'PSW')
        self.safe_append(winner_betting_odds, match, 'SBW')
        self.safe_append(winner_betting_odds, match, 'SJW')
        self.safe_append(winner_betting_odds, match, 'UBW')

        self.safe_append(loser_betting_odds, match, 'B365L')
        self.safe_append(loser_betting_odds, match, 'B&WL')
        self.safe_append(loser_betting_odds, match, 'CBL')
        self.safe_append(loser_betting_odds, match, 'EXL')
        self.safe_append(loser_betting_odds, match, 'LBL')
        self.safe_append(loser_betting_odds, match, 'GBL')
        self.safe_append(loser_betting_odds, match, 'IWL')
        self.safe_append(loser_betting_odds, match, 'PSL')
        self.safe_append(loser_betting_odds, match, 'SBL')
        self.safe_append(loser_betting_odds, match, 'SJL')
        self.safe_append(loser_betting_odds, match, 'UBL')
        return winner_betting_odds, loser_betting_odds

    def safe_append(self, lst, match, bet_exchange):
        try:
            lst.append(match[bet_exchange])
        except KeyError as e:
            pass


    def update_match_statistics(self, current_money, earnings, match):
        roi = self.calculate_ROI(current_money + earnings, match)
        self.total_bets +=1
        return

    def get_run_data(self):
        return self.atp_matches, self.wta_matches

    def data_to_list(df):
        return df.to_dict('records')
