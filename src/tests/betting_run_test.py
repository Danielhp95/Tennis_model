import unittest
import inspect
import os, sys
import pandas as pd
betting_path = os.path.abspath(os.path.join('..'))
sys.path.append(betting_path)
from betting import betting_run

import test_data.betting_strategies 
sys.path.append(os.path.abspath(os.path.join('test_data','betting_strategies')))
import strategies as st
sys.path.append(os.path.abspath(os.path.join('test_data','betting_models')))
import test_models as md

class betting_run_test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        return

    def test_can_filter_on_many_fields(self):
        initial_money = 1
        mo         = md.FiftyFiftyModel()
        strat      = st.BetOnLoserStrategy()

        earliest_year = 2007
        latest_year   = 2007
        courts        = ['Grass']
        tournaments   = 'Open Seat Godo'
        players       = 'Federer R'
        rounds        = '1st Round'
        best_of       = 3
        rank_position = 50
        rank_points   = 50
        btr = betting_run.BettingRun(initial_money=initial_money,
                                     earliest_year=earliest_year, latest_year=latest_year,
                                     courts=courts, tournaments=tournaments, players=players,
                                     rounds=rounds, best_of=best_of, rank_position=rank_position,
                                     rank_points=rank_points,
                                     model=mo, strategy=strat)

        assert len(btr.atp_matches) > len(btr.atp_bet)

    def test_run_ends_if_no_money(self):
        strat = st.BetOnLoserStrategy()
        model = md.FiftyFiftyModel()
        btr = betting_run.BettingRun(initial_money=1,
                                     earliest_year=2007, latest_year=2007,
                                     model=model,
                                     strategy=strat)
        btr.betting_run()
        assert btr.total_bets == 1


    def test_bet_matches_ascend_in_date(self):
        # test assertion made in strategy
        strat = st.RecordDatesStrategy()
        model = md.FiftyFiftyModel()
        btr = betting_run.BettingRun(initial_money=1,
                                     earliest_year=2007, latest_year=2007,
                                     model=model,
                                     strategy=strat)
        btr.atp_bet = btr.atp_bet[100:400] # reduces testing time
        btr.betting_run()
        
    def test_calculate_match_odds(self):
        strat = st.RecordDatesStrategy()
        model = md.FiftyFiftyModel()
        btr = betting_run.BettingRun(initial_money=1,
                                     earliest_year=2007, latest_year=2007,
                                     model=model,
                                     strategy=strat)
        match_odds = pd.DataFrame(zip([1],[1]), columns=['B365W','B365L'])
        w_odds, l_odds = btr.match_betting_odds(match_odds.loc[0]) 
        assert len(w_odds) == 1 and w_odds[0] ==1
        assert len(l_odds) == 1 and l_odds[0] == 1

    def test_safe_append(self):
        strat = st.RecordDatesStrategy()
        model = md.FiftyFiftyModel()
        btr = betting_run.BettingRun(initial_money=1,
                                     earliest_year=2007, latest_year=2007,
                                     model=model,
                                     strategy=strat)
        lst = []
        btr.safe_append([], pd.DataFrame(zip([1],[1])), 'NoneExistent')
        assert lst == []

    def test_statistics_total_bets(self):
        strat = st.BetOnWinnerStrategy()
        model = md.FiftyFiftyModel()
        btr = betting_run.BettingRun(initial_money=1,
                                     earliest_year=2007, latest_year=2007,
                                     model=model,
                                     strategy=strat)
        btr.betting_run()
        num_matches = len(btr.atp_bet)
        #TODO: change to equals when combine tables work
        assert btr.total_bets <= num_matches

    #def test_statistics_bet_amount(self):
    #    pass

    #def test_statistics_earnings(self):
    #    initial_money = 1
    #    btr = self.create_betting_run(st.BetOnWinnerStrategy, md.FiftyFiftyModel,
    #                                  initial_money=initial_money)
    #    btr.betting_run()

    #    for match, stats in btr.matches_statistics['ATP'][]:
            

    def test_statistics_money(self):
        initial_money = 2000
        btr = self.create_betting_run(st.BetOnWinnerStrategy, md.FiftyFiftyModel,
                                      initial_money = initial_money)
        btr.betting_run()
        current_money = initial_money
        for match, stats in btr.matches_statistics['ATP']:
            assert current_money == stats['money']
            current_money += stats['earnings']

    def test_statistics_player_bet_against(self):
        btr = self.create_betting_run(st.BetOnWinnerStrategy, md.FiftyFiftyModel)
        btr.betting_run()
        for match, stats in btr.matches_statistics['ATP']:
            assert match['winner_name'] == stats['player_bet']

    #def test_statistics_model_odds(self):
    #    pass

    def create_betting_run(self, strat, mod, initial_money=1):
        strat = strat()
        model = mod()
        return  betting_run.BettingRun(initial_money=initial_money,
                                     earliest_year=2007, latest_year=2007,
                                     model=model, strategy=strat)

