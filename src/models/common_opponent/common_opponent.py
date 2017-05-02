from __future__ import division

import os, sys
#omalley_path = os.path.abspath(os.path.join('..', 'omalley'))
omalley_path = os.path.abspath(os.path.join('..'))
sys.path.append(omalley_path)
import omalley.omalley as omalley
tennis_atp_dao_path = os.path.abspath(os.path.join('..','daos'))
sys.path.append(tennis_atp_dao_path)
import tennisAtpDao as dao

"""
  Common opponent model
  Authors: William J. Knottenbelt, Demitris Spanias & Agnieszka M. Madurska
"""
class CommonOpponent(object):

    def __init__(self, model_function=omalley.M3, best_of=3):
        self.model_function = model_function if best_of == 3 else omalley.M5
        self.average_player_performance = 0.6
        self.com_ops = None
        self.MIN_OPP_THRESHOLD = 4
        self.latest_year      = 2017 # change once a year
        self.earliest=_year   = 2017
        self.courts = ["Hard", "Clay", "Grass", "Carpet"] #TODO Ask Wil if there are more courts

    def check_min_opponent_threshold(self, com_ops_set):
        print("Common opponents: " + str(len(com_ops_set)))
        if len(com_ops_set) < self.MIN_OPP_THRESHOLD:
            print("Minimum amount of common opponents " + 
                   str(self.MIN_OPP_THRESHOLD) + " given " + 
                   str(len(com_ops_set)))
            return -1
        return 0

    def win_probability(self, player_a, player_b, prob_type):
        f_opponents = self.com_ops[((self.com_ops.winner_name == player_a) & (self.com_ops.loser_name == player_b)) |
                                   ((self.com_ops.winner_name == player_b) & (self.com_ops.loser_name == player_a))]
        
        wp = -1
        if len(f_opponents) >= 1: # Do average over all cases
            wp = self.multiple_match_swp(player_a, f_opponents) if prob_type == "swp" else self.multiple_match_rwp(player_a, f_opponents)
        elif len(f_opponents) == 1: # Normal case
            wp = self.single_swp(player_a, f_opponents, 0) if prob_type == "swp" else self.single_rwp(player_a, f_opponents, 0)

        return wp

    def single_swp(self, player_a, df, i):
        if df.winner_name[i] == player_a:
            return (df.w_1stWon[i] + df.w_2ndWon[i]) / df.w_svpt[i]
        else:
            return (df.l_1stWon[i] + df.l_2ndWon[i]) / df.l_svpt[i]

    def multiple_match_swp(self, player_a, df):
        return sum([self.single_swp(player_a, df, i) 
                    for i, _ in df.iterrows()]) / len(df)

    def single_rwp(self, player_a, df, i):
        if df.winner_name[i] == player_a:
            return 1 - ((df.l_1stWon[i] + df.l_2ndWon[i]) / df.l_svpt[i])
        else:
            return 1 - ((df.w_1stWon[i] + df.w_2ndWon[i]) / df.w_svpt[i])

    def multiple_match_rwp(self, player_a, df):
        return sum([self.single_rwp(player_a, df, i) 
                    for i, _ in df.iterrows()]) / len(df)

    def advantage_via_com_opp(self, player_a, player_b, com_opp):
        spw_a = self.win_probability(player_a, com_opp, "swp")
        spw_b = self.win_probability(player_b, com_opp, "swp")
        rpw_a = self.win_probability(player_a, com_opp, "rwp") #?
        rpw_b = self.win_probability(player_b, com_opp, "rwp") #?
        return (spw_a - (1 - rpw_a)) - (spw_b - (1 - rpw_b))

    def prob_beating_through_com_opp(self, player_a, player_b, com_opp):
        delta_a_b_c = self.advantage_via_com_opp(player_a, player_b, com_opp)
        print((delta_a_b_c, com_opp))
        pos_effect = self.average_player_performance + delta_a_b_c
        effect_on_player_a = self.model_function(pos_effect, 1-0.6)

        neg_effect = 1 - (0.6 + delta_a_b_c)
        effect_on_player_b = self.model_function(0.6, neg_effect)

        return 0.5 * (effect_on_player_a + effect_on_player_b)

    def prob_a_beating_b(self, player_a, player_b):
        com_ops_set, self.com_ops = dao.common_opponents(player_a, player_b,
                                                         latest_year=self.latest_year,
                                                         earliest_year=self.earliest_year, 
                                                         courts=self.courts)

        if self.check_min_opponent_threshold(com_ops_set) == -1:
            return -1

        probabilities = [self.prob_beating_through_com_opp(player_a, player_b, op)
                 for op in com_ops_set]
        print(zip(probabilities, com_ops_set))
        normalized_probability = sum(probabilities) / len(com_ops_set)
        return normalized_probability

if __name__ == '__main__':
    com = CommonOpponent()
    com.courts        = ["Hard", "Clay"]
    com.earliest_year = 2014
    com.latest_year   = 2017

    p = com.prob_a_beating_b('Roger Federer' ,'Nikoloz Basilashvili')
    print(p)

