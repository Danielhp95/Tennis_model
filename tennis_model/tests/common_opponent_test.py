from __future__ import division

import unittest
import os, sys
import pandas as pd
models_path = os.path.abspath(os.path.join('..'))
sys.path.append(models_path)
from  models.common_opponent import common_opponent as co

class common_opponent_test(unittest.TestCase):

    # Have tests for different input model functions?
    @classmethod
    def setUpClass(self):
        self.com = co.CommonOpponent()

    def test_calculate_single_swp_player_winner(self):
        f = 'single_swp_winner.csv'
        swp = self.calculate_swp_from_loc_player(f, 'Simon Greul')
        real_swp = (14 + 25) / 57
        assert(real_swp == swp)

    def test_calculate_single_swp_player_loser(self):
        f = 'single_swp_loser.csv' 
        swp = self.calculate_swp_from_loc_player(f, 'Simon Greul')
        real_swp = (14 + 25) / 57
        assert(real_swp == swp)

    def test_calculate_multiple_swp_winner(self):
        f = 'multiple_match_swp_winner.csv'
        swp = self.calculate_swp_from_loc_player(f, 'Simon Greul')
        real_swp = (((14 + 25) / 57) + ((15 + 20) /50)) * 0.5 
        assert(real_swp == swp)

    def test_calculate_multiple_swp_mixed(self):
        f = 'multiple_match_swp_mixed.csv'
        swp = self.calculate_swp_from_loc_player(f, 'Simon Greul')
        real_swp = (((14 + 25) / 57) + ((22 + 11) /64)) * 0.5 
        assert(real_swp == swp)

    def calculate_swp_from_loc_player(self, loc, player):
        location = r'test_data/' + loc
        df = pd.read_csv(location, skipinitialspace=True)
        if len(df) > 1:
            return self.com.multiple_match_swp(player, df)
        else:
            return self.com.single_swp(player, df, 0)

    #filtering
    def test_service_win_probability_filters_players(self):
        f = 'single_match_filter_out.csv'
        swp = self.calculate_wp_from_players(f,'Stanislas Wawrinka', 'RF', "swp")
        real_swp = -1 # Error, no common opponents
        assert(real_swp == swp)

    #single match
    def test_swp_single_match(self):
        f = 'single_match_with_filtering.csv'
        swp = self.calculate_wp_from_players(f,'Simon Greul', 'Paolo Lorenzi',"swp")
        real_swp = (14 + 25) / 57
        assert(real_swp == swp)
          
    #multiple matches
    def test_swp_multiple_match(self):
        f = 'multiple_match_swp_with_filtering.csv'
        swp = self.calculate_wp_from_players(f,'Simon Greul', 'Paolo Lorenzi', "swp")
        real_swp = (((14 + 25) / 57) + ((14 + 25) / 58))*0.5
        assert(real_swp == swp)

    def calculate_wp_from_players(self, loc, player_a, player_b, prob_type):
        loc = r'test_data/' + loc
        self.com.com_ops = pd.read_csv(loc, skipinitialspace=True)
        return self.com.win_probability(player_a, player_b, prob_type)

############# RWP tests #######################################

    def test_rpw_single_match_winner(self):
        f = 'single_swp_winner.csv'
        rpw = self.calculate_rwp_from_loc_player(f,'Simon Greul')
        real_rpw = 1 - ((22 + 11) /64)
        assert(real_rpw == rpw)

    def test_rpw_single_match_winner(self):
        f = 'single_swp_loser.csv'
        rpw = self.calculate_rwp_from_loc_player(f,'Simon Greul')
        real_rpw = 1 - ((25 + 14) /57)
        assert(real_rpw == rpw)

    def calculate_rwp_from_loc_player(self, loc, player):
        location = r'test_data/' + loc
        df = pd.read_csv(location, skipinitialspace=True)
        if len(df) > 1:
            return self.com.multiple_match_rwp(player, df)
        else:
            return self.com.single_rwp(player, df, 0)

if __name__ == '__main__':
    unittest.main()
