import unittest
import os, sys
markov_path = os.path.abspath(os.path.join('..','simulators','markov_chains'))
sys.path.append(markov_path)
import numpy as np
import game_level as gl

class GameLevelTest(unittest.TestCase):

    def test_is_not_over(self):
        self.assert_is_over_outcome(goal=3, lead=0, state=(0,0), outcome=0)
        self.assert_is_over_outcome(goal=3, lead=0, state=(1,0), outcome=0)
        self.assert_is_over_outcome(goal=3, lead=0, state=(1,1), outcome=0)
        self.assert_is_over_outcome(goal=3, lead=0, state=(2,0), outcome=0)
        self.assert_is_over_outcome(goal=3, lead=0, state=(2,1), outcome=0)
        self.assert_is_over_outcome(goal=3, lead=0, state=(2,2), outcome=0)

        self.assert_is_over_outcome(goal=3, lead=0, state=(0,1), outcome=0)
        self.assert_is_over_outcome(goal=3, lead=0, state=(1,2), outcome=0)
        self.assert_is_over_outcome(goal=3, lead=0, state=(1,2), outcome=0)

    def test_is_not_over_within_lead(self):
        self.assert_is_over_outcome(goal=5, lead=3, state=(5,2), outcome=1)
        self.assert_is_over_outcome(goal=5, lead=3, state=(6,3), outcome=1)
        self.assert_is_over_outcome(goal=5, lead=3, state=(7,4), outcome=1)

        self.assert_is_over_outcome(goal=5, lead=3, state=(5,3), outcome=2)
        self.assert_is_over_outcome(goal=5, lead=3, state=(5,4), outcome=2)
        self.assert_is_over_outcome(goal=5, lead=3, state=(6,4), outcome=2)
        self.assert_is_over_outcome(goal=5, lead=3, state=(6,5), outcome=2)

        self.assert_is_over_outcome(goal=5, lead=3, state=(2,5), outcome=-1)
        self.assert_is_over_outcome(goal=5, lead=3, state=(3,6), outcome=-1)
        self.assert_is_over_outcome(goal=5, lead=3, state=(4,7), outcome=-1)

        self.assert_is_over_outcome(goal=5, lead=3, state=(3,5), outcome=-2)
        self.assert_is_over_outcome(goal=5, lead=3, state=(4,5), outcome=-2)
        self.assert_is_over_outcome(goal=5, lead=3, state=(4,6), outcome=-2)
        self.assert_is_over_outcome(goal=5, lead=3, state=(5,6), outcome=-2)

    def test_is_not_over(self):
        self.assert_is_over_outcome(goal=8, lead=3, state=(7,5), outcome=0)

    def test_is_over_winner_a_normal(self):
        self.assert_is_over_outcome(goal=3, lead=0, state=(3,0), outcome=1)
        self.assert_is_over_outcome(goal=3, lead=0, state=(3,1), outcome=1)
        self.assert_is_over_outcome(goal=3, lead=0, state=(3,2), outcome=1)

    def test_is_over_winner_b_normal(self):
        self.assert_is_over_outcome(goal=3, lead=0, state=(0,3), outcome=-1)
        self.assert_is_over_outcome(goal=3, lead=0, state=(1,3), outcome=-1)
        self.assert_is_over_outcome(goal=3, lead=0, state=(2,3), outcome=-1)

    def test_is_over_winner_a_golden_point(self):
        self.assert_is_over_outcome(goal=5, lead=3, golden=8, state=(8,7), outcome=3)
        self.assert_is_over_outcome(goal=5, lead=3, golden=8, state=(8,6), outcome=3)

    def test_is_over_winner_a_golden_point(self):
        self.assert_is_over_outcome(goal=5, lead=3, golden=8, state=(6,8), outcome=-3)
        self.assert_is_over_outcome(goal=5, lead=3, golden=8, state=(7,8), outcome=-3)

    def test_is_over_number_of_serves(self):
        self.assert_is_over_outcome(goal=3, lead=2, number_of_serves=2, state=(3,3), outcome=2)

    ### Test for probability propagation functionality ###

    # This is one of the most basic scenarios. There is no golden point
    # and all valid indexes are adjacent
    def test_calculate_states_from_indexes(self):
        g = gl.GameLevel(best_of=3)
        g.wp = 1
        g.lp = -1
        number_of_transient_states = 4
        valid_indexes = [0,6,12,18]
        real_st_to_in = {(0,0):0,(1,0):6,(0,1):12,(1,1):18}
        real_in_to_st = {0:(0,0),6:(1,0),12:(0,1),18:(1,1)}
        in_to_st, st_to_in = g.calculate_states_from_indexes(number_of_transient_states, valid_indexes)
        assert real_st_to_in == st_to_in
        assert real_in_to_st == in_to_st

    def test_calculate_states_from_indexes_tiebreaker_serve(self):
        g = gl.GameLevel(goal=2,lead=2,number_of_serves=2)
        g.wp = 1
        g.lp = -1
        number_of_transient_states = 4
        valid_indexes = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        real_st_to_in = {(0,0):0,
                         (1,0):1,
                         (0,1):2,
                         ('adv',(0,'a',0)):3,
                         ('adv',(0,'a',1)):4,
                         ('adv',(0,'b',0)):5,
                         ('adv',(0,'b',1)):6,
                         ('adv',(1,'a',0)):7,
                         ('adv',(1,'a',1)):8,
                         ('adv',(1,'b',0)):9,
                         ('adv',(1,'b',1)):10,
                         ('adv',(-1,'a',0)):11,
                         ('adv',(-1,'a',1)):12,
                         ('adv',(-1,'b',0)):13,
                         ('adv',(-1,'b',1)):14}

        real_in_to_st = {k:v for v,k in real_st_to_in.items()}

        in_to_st, st_to_in = g.calculate_states_from_indexes(number_of_transient_states, valid_indexes)
        assert real_st_to_in == st_to_in
        assert real_in_to_st == in_to_st


    ### Util functions ###
    def assert_is_over_outcome(self, goal=None, lead=None, golden=float("inf"),
                                          best_of=None, number_of_serves=None, state=None, outcome=None):
        g = gl.GameLevel(goal, lead, golden, best_of, number_of_serves)
        assert outcome == g.is_over(state, goal, lead, golden, best_of, number_of_serves)

    def create_trans_matrix_only_goal(self, wp, lp):
        # goal=3, lead=0
        win_index = 9
        lose_index = 10
        trans_m = np.zeros((9,11))
        trans_m[0][1] = wp
        trans_m[0][2] = lp
        trans_m[1][3] = wp
        trans_m[1][4] = lp
        trans_m[2][4] = wp
        trans_m[2][5] = lp
        trans_m[3][win_index] = wp
        trans_m[3][6] = lp
        trans_m[4][6] = wp
        trans_m[4][7] = lp
        trans_m[5][7] = wp
        trans_m[5][lose_index] = lp
        trans_m[6][win_index] = wp
        trans_m[6][8] = lp
        trans_m[7][8] = wp
        trans_m[7][lose_index] = lp
        trans_m[8][win_index] = wp
        trans_m[8][lose_index] = lp
        return trans_m

    def create_trans_matrix_lead_2(self, wp, lp):
        # goal=3, lead=2
        win_index = 11
        lose_index = 12
        trans_m = np.zeros((11,13))
        trans_m[0][1] = wp
        trans_m[0][2] = lp
        trans_m[1][3] = wp
        trans_m[1][4] = lp
        trans_m[2][4] = wp
        trans_m[2][5] = lp
        trans_m[3][win_index] = wp
        trans_m[3][6] = lp
        trans_m[4][6] = wp
        trans_m[4][7] = lp
        trans_m[5][7] = wp
        trans_m[5][lose_index] = lp
        trans_m[6][win_index] = wp
        trans_m[6][8] = lp
        trans_m[7][8] = wp
        trans_m[7][lose_index] = lp
        trans_m[8][9] = wp
        trans_m[8][10] = lp
        trans_m[9][win_index] = wp
        trans_m[9][8] = lp
        trans_m[10][8] = wp
        trans_m[10][lose_index] = lp
        return trans_m


