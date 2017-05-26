import unittest
import os, sys
markov_path = os.path.abspath(os.path.join('..','simulators','markov_chains'))
sys.path.append(markov_path)
import numpy as np
import game_level as gl

class GameLevelTest(unittest.TestCase):

    def test_initialization(self):
        pass

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


    ### Tests for mark_outcome functionality ###
    def test_mark_outcome_normal(self):
        g = gl.GameLevel(goal=3)
        g.states_populated = {}

        outcome   = 0
        state     = (1,0)
        cur_index = 0
        av_i      = [1]
        trans_m   = np.array([[0,0]])
        p         = 1
        g.mark_outcome(outcome, (state[0] +1, state[1]), cur_index, av_i, trans_m, p)

        assert av_i == []
        assert g.states_populated == {1:(2,0), (2,0):1}
        np.testing.assert_allclose(trans_m, np.array([[0,p]]))

    def test_mark_outcome_win_a(self):
        g = gl.GameLevel(goal=3)
        g.states_populated = {}
        g.win_index = 1

        outcome   = 1
        cur_index = 0
        av_i      = [1]
        trans_m   = np.array([[0,0]])
        p         = 1
        g.mark_outcome(outcome, None, cur_index, av_i, trans_m, p)

        assert av_i == [1]
        assert g.states_populated == {}
        np.testing.assert_allclose(trans_m, np.array([[0,p]]))

    def test_mark_outcome_win_b(self):
        g = gl.GameLevel(goal=3)
        g.states_populated = {}
        g.lose_index = 1

        outcome   = -1
        cur_index = 0
        av_i      = [1]
        trans_m   = np.array([[0,0]])
        p         = 1
        g.mark_outcome(outcome, None, cur_index, av_i, trans_m, p)

        assert av_i == [1]
        assert g.states_populated == {}
        np.testing.assert_allclose(trans_m, np.array([[0,p]]))

    ### Test for probability propagation functionality ###

    # This is one of the most basic scenarios. There is no golden point
    # and all valid indexes are adjacent
    def test_populate_transitions_only_goal(self):
        goal   = 3
        lead   = 0
        g = gl.GameLevel(goal, lead)
        g.wp = 1
        g.lp = -1
        trans_matrix = np.zeros((9,11))
        num_trans_states = 9
        valid_indexes    = range(0,num_trans_states)
        win_i  = 9
        lose_i = 10
        g.populate_transition_matrix(trans_matrix, num_trans_states, valid_indexes,
                                     win_i, lose_i)
        real_final_trans_matrix = self.create_trans_matrix_only_goal(g.wp, g.lp)
        np.testing.assert_allclose(real_final_trans_matrix, trans_matrix, rtol=1e-1)

    def test_populate_transitions_lead(self):
        goal   = 3
        lead   = 2
        g = gl.GameLevel(goal, lead)
        g.wp = 1
        g.lp = -1
        trans_matrix = np.zeros((11,13))
        num_trans_states = 11
        valid_indexes    = range(0,num_trans_states)
        win_i  = 11
        lose_i = 12
        g.populate_transition_matrix(trans_matrix, num_trans_states, valid_indexes,
                                     win_i, lose_i)
        real_final_trans_matrix = self.create_trans_matrix_lead_2(g.wp, g.lp)
        print(real_final_trans_matrix)
        print(trans_matrix)
        np.testing.assert_allclose(real_final_trans_matrix, trans_matrix, rtol=1e-1)

    def test_populate_transitions_lead_golden(self):
        goal   = 4
        lead   = 2
        golden = 6
        g = gl.GameLevel(goal, lead, golden)
        g.wp = 1
        g.lp = -1
        trans_matrix = np.zeros((22,24))
        num_trans_states = 22
        valid_indexes    = range(0,num_trans_states)
        print(len(valid_indexes))
        win_i  = 22
        lose_i = 23
        g.populate_transition_matrix(trans_matrix, num_trans_states, valid_indexes,
                                     win_i, lose_i)
        real_final_trans_matrix = self.create_trans_matrix_lead_golden(g.wp, g.lp)
        np.testing.assert_allclose(real_final_trans_matrix, trans_matrix, rtol=1e-1)


    ### Util functions ###
    def assert_is_over_outcome(self, goal=None, lead=None, golden=float("inf"),
                                          best_of=None, state=None, outcome=None):
        g = gl.GameLevel(goal, lead, golden, best_of)
        assert outcome == g.is_over(state, goal, lead, golden, best_of)

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

    # TODO:FIGURE THIS OUT
    def create_trans_matrix_lead_3(self, wp, lp):
        # goal=4, lead=3
        win_index = 20
        lose_index = 21
        trans_m = np.zeros((20,22))
        trans_m[0][1] = wp
        trans_m[0][2] = lp
        trans_m[1][3] = wp
        trans_m[1][4] = lp
        trans_m[2][4] = wp
        trans_m[2][5] = lp
        trans_m[3][6] = wp
        trans_m[3][7] = lp
        trans_m[4][7] = wp
        trans_m[4][8] = lp
        trans_m[5][8] = wp
        trans_m[5][9] = lp
        trans_m[6][win_index] = wp
        trans_m[6][10] = lp
        trans_m[7][10] = wp
        trans_m[7][11] = lp
        trans_m[8][11] = wp
        trans_m[8][12] = lp
        trans_m[9][12] = wp
        trans_m[9][lose_index] = lp
        trans_m[11][win_index] = wp
        trans_m[10][13] = lp
        trans_m[11][13] = wp
        trans_m[11][14] = lp
        trans_m[12][14] = wp
        trans_m[12][lose_index] = lp
        trans_m[13][4] = wp
        trans_m[13][1] = wp
        trans_m[14][2] = lp
        trans_m[14][3] = wp
        trans_m[15][4] = lp
        trans_m[15][4] = wp
        trans_m[16][1] = wp
        trans_m[16][2] = lp
        trans_m[17][3] = wp
        trans_m[17][4] = lp
        trans_m[18][4] = wp
        trans_m[18][1] = wp
        trans_m[19][2] = lp
        trans_m[19][3] = wp
        return trans_m

    def create_trans_matrix_lead_golden(self, wp, lp):
        # goal = 4, lead= 2, golden = 6
        win_index = 22
        lose_index = 23
        trans_m = np.zeros((22,24))

        trans_m[0][1] = wp
        trans_m[0][2] = lp
        trans_m[1][3] = wp
        trans_m[1][4] = lp
        trans_m[2][4] = wp
        trans_m[2][5] = lp
        trans_m[3][6] = wp
        trans_m[3][7] = lp
        trans_m[4][7] = wp
        trans_m[4][8] = lp
        trans_m[5][8] = wp
        trans_m[5][9] = lp
        trans_m[6][win_index] = wp
        trans_m[6][10] = lp
        trans_m[7][10] = wp
        trans_m[7][11] = lp
        trans_m[8][11] = wp
        trans_m[8][12] = lp
        trans_m[9][12] = wp
        trans_m[9][lose_index] = lp
        trans_m[10][win_index] = wp
        trans_m[10][13] = lp
        trans_m[11][13] = wp
        trans_m[11][14] = lp
        trans_m[12][14] = wp
        trans_m[12][lose_index] = lp
        trans_m[13][win_index] = wp
        trans_m[13][15] = lp
        trans_m[14][15] = wp
        trans_m[14][lose_index] = lp
        trans_m[15][16] = wp
        trans_m[15][17] = lp
        trans_m[16][win_index] = wp
        trans_m[16][18] = lp
        trans_m[17][18] = wp
        trans_m[17][lose_index] = lp
        trans_m[18][19] = wp
        trans_m[18][20] = lp
        trans_m[19][win_index] = wp
        trans_m[19][21] = lp
        trans_m[20][21] = wp
        trans_m[20][lose_index] = lp
        trans_m[21][win_index] = wp
        trans_m[21][lose_index] = lp
        return trans_m
