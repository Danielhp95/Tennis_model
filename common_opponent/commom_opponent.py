from __future__ import division

import os, sys
omalley_path = os.path.abspath(os.path.join('..', 'omalley'))
sys.path.append(omalley_path)
import omalley
tennis_atp_dao_path = os.path.abspath(os.path.join('..', 'data','dao'))
sys.path.append(tennis_atp_dao_path)
import tennisAtpDao as dao


"""
  Common opponent model
  Authors: William J. Knottenbelt, Demitris Spanias & Agnieszka M. Madurska
"""
class CommonOpponnent(object):

    def __init__(self, model_function=omalley.M3, best_of=3):
        self.model_function = model_function if best_of == 3 else omalley.M5
        self.average_player_performance = 0.6
        self.com_ops = None
        self.MIN_OPP_THRESHOLD = 4


    def service_win_probability(self, player_a, player_b):
        f_opponents = self.com_ops[((self.com_ops.winner_name == player_a) & (self.com_ops.loser_name == player_b)) |
                                   ((self.com_ops.winner_name == player_b) & (self.com_ops.loser_name == player_a))]
        
        swp = -1
        if len(f_opponents) >= 1: # Do average over all cases
            swp = sum([self.single_swp(player_a, f_opponents, index) for index, row in f_opponents.iterrows()]) / len(f_opponents)
        elif len(f_opponents) == 1: # Normal case
            swp = self.single_swp(player_a, f_opponents, 0)
        else: #Should never get here
            print("Error no common opponents")

        assert(swp >= 0)

        return swp

    def single_swp(self, player_a, df, i):
        if df.winner_name[i] == player_a:
            return (df.w_1stWon[i] + df.w_2ndWon[i]) / df.w_svpt[i]
        else:
            return (df.l_1stWon[i] + df.l_2ndWon[i]) / df.l_svpt[i]


    def advantage_via_com_opp(self, player_a, player_b, com_opp):
        spw_a = self.service_win_probability(player_a, com_opp)
        spw_b = self.service_win_probability(player_b, com_opp)
        rpw_a = 1 - self.service_win_probability(com_opp, player_a)
        rpw_b = 1 - self.service_win_probability(com_opp, player_b)
        return (spw_a - rpw_a) - (spw_b - rpw_b)

    def prob_beating_through_com_opp(self, player_a, player_b, com_opp):
        delta_a_b_c = self.advantage_via_com_opp(player_a, player_b, com_opp)
        
        pos_effect = self.average_player_performance + delta_a_b_c
        effect_on_player_a = self.model_function(pos_effect, 1-0.6)

        neg_effect = 1 - (0.6 + delta_a_b_c)
        effect_on_player_b = self.model_function(0.6, neg_effect)

        return 0.5 * (effect_on_player_a + effect_on_player_b)

    def prob_a_beating_b(self, player_a, player_b, since):
        com_ops_set, self.com_ops = dao.common_opponents(player_a, player_b, since)

        print("Common opponents: " + str(len(com_ops_set)))
        if len(com_ops_set) < self.MIN_OPP_THRESHOLD:
            print("Minimum amount of common opponents " + 
                   str(self.MIN_OPP_THRESHOLD) + " given " + 
                   str(len(com_ops_set)))
            return -1
        probs = [self.prob_beating_through_com_opp(player_a, player_b, op)
                 for op in com_ops_set]
        return sum(probs) / len(com_ops_set)  

com = CommonOpponnent()
p = com.prob_a_beating_b('Nikoloz Basilashvili', 'Roger Federer' ,2015)
print(p)

