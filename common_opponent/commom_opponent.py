import os, sys
omalley_path = os.path.abspath(os.path.join('..', 'omalley'))
sys.path.append(omalley_path)
import omalley

"""
  Common opponent model
  Authors: William J. Knottenbelt, Demitris Spanias & Agnieszka M. Madurska
"""
class CommonOpponnent(object):

    def __init__(self, model_function=omalley.M3, best_of=3, dao=None):
        self.model_function = model_function if best_of == 3 else omalley.M5
        self.dao = dao
        self.average_player_performance = 0.6

        #TODO: implement common opponent calculation.

    #TODO: implement once I have point by point data
    def service_win_probability(self, player_A, player_B):
        return 0

    def advantage_via_com_opp(self, player_A, player_B, com_opp):
        spw_a = self.service_win_probability(player_A, com_opp)
        spw_b = self.service_win_probability(player_B, com_opp)
        rpw_a = 1 - service_win_probability(com_opp, player_A)
        rpw_b = 1 - service_win_probability(com_opp, player_B)
        return (spw_a - rpw_a) - (spw_b - rpw_b)

    def prob_beating_through_com_opp(self, player_A, player_B, comm_opp):
        delta_a_b_c = self.advantage_via_com_opp(player_A, player_B, com_opp)

        pos_effect = self.average_player_performance + delta_a_b_c
        effect_on_player_a = self.model_function(pos_effect, 1-0.6)

        neg_effect = 1 - (0.6 + delta_a_b_c)
        effect_on_player_b = self.model_function(0.6, neg_effect)

        return 0.5 * (effect_on_player_a - effect_on_player_b)

    def prob_a_beating_b(self, player_a, player_b, com_opps):
        probs = [self.prob_beating_through_com_opp(player_a, player_b, op)
                 for op in com_opps]
        return sum(probs) / len(probs)  

