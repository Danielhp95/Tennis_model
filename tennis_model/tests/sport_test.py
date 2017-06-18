import unittest
import os, sys
markov_path = os.path.abspath(os.path.join('..','simulators','markov_chains'))
sys.path.append(markov_path)
import numpy as np
import game_level as gl
import sport as sp

class SportTest(unittest.TestCase):

    #### Calculate game sizes ###

    def test_size_best_of_only(self):
        self.assert_game_level_size(best_of=3, expected_size=4)
        self.assert_game_level_size(best_of=5, expected_size=9)

    def test_size_goal_only(self):
        self.assert_game_level_size(goal=1, lead=0, golden=0, expected_size=1)
        self.assert_game_level_size(goal=2, lead=0, golden=0, expected_size=4)
        self.assert_game_level_size(goal=3, lead=0, golden=0, expected_size=9)
        self.assert_game_level_size(goal=5, lead=0, golden=0, expected_size=25)
        self.assert_game_level_size(goal=8, lead=0, golden=0, expected_size=64)

    def test_size_goal_lead(self):
        self.assert_game_level_size(goal=3, lead=2, golden=0, expected_size=11)
        self.assert_game_level_size(goal=4, lead=2, golden=0, expected_size=18)
        self.assert_game_level_size(goal=4, lead=3, golden=0, expected_size=20)

    def test_size_goal_lead_golden(self):
        self.assert_game_level_size(goal=2, lead=2, golden=6, expected_size=16)
        self.assert_game_level_size(goal=3, lead=2, golden=7, expected_size=21)
        self.assert_game_level_size(goal=4, lead=2, golden=6, expected_size=22)
        self.assert_game_level_size(goal=4, lead=3, golden=8, expected_size=36)

    def test_size_goal_lead_numberOfServes(self):
        self.assert_game_level_size(goal=2, lead=2, number_of_serves=2, expected_size=15)
        self.assert_game_level_size(goal=3, lead=2, number_of_serves=2, expected_size=20)
        # If Lead is zero, then number of serves is ignored, because it is multiplied by Lead
        self.assert_game_level_size(goal=8, lead=0, golden=0, number_of_serves=3, expected_size=64)
        self.assert_game_level_size(goal=4, lead=3, golden=8, number_of_serves=2, expected_size=36)

    def assert_game_level_size(self,goal=0, lead=0, golden=float('inf'),
                               best_of=None, number_of_serves=None,expected_size=-1):
        s = sp.Sport()
        size = s.calculate_number_of_states(goal, lead, golden, best_of, number_of_serves=number_of_serves)
        assert size == expected_size

    #### Creating valid indexes ###

    def test_generate_isolated_level_sizes(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=3)
        s.add_hierarchy_level(goal=4, lead=2)
        isolated_level_sizes = s.isolated_level_size()
        assert isolated_level_sizes == [4, 18]

    def test_generat_aggregated_level_size(self):
        s = sp.Sport()
        isolated_level_sizes = [5,3,2]
        total_level_sizes    = s.aggregated_level_size(isolated_level_sizes)
        assert total_level_sizes == [30,6,2]

    def test_generate_all_valid_indexes(self):
        s = sp.Sport()
        isolated_level_sizes = [4,3,2]
        total_level_sizes    = [24,6,2]
        real_valid_indexes   = [[[0,6,12,18]],
                                [[0,2,4],[6,8,10],[12,14,16],[18,20,22]],
                                [[0,1],[2,3],[4,5],[6,7],[8,9],[10,11],[12,13],[14,15],[16,17],[18,19],[20,21],[22,23]]]
        valid_indexes = s.generate_all_valid_indexes(isolated_level_sizes, total_level_sizes)
        assert valid_indexes == real_valid_indexes

    def test_calculate_absolute_state_from_relative_basic(self):
        s = sp.Sport()
        relative_state       = (0,0) 
        isolated_level_sizes = [4]
        total_level_sizes    = [4]
        valid_indexes   = [[[0,1,2,3]]]
        absolute_state  = s.absolute_state_from_relative(relative_state, 0, 0, valid_indexes, {})

        assert absolute_state == [(0,0)]

    def test_calculate_absolute_state_from_relative_two_levels(self):
        s = sp.Sport()
        relative_state       = (0,1) 
        isolated_level_sizes = [4,4]
        total_level_sizes    = [16,4]
        valid_indexes   = [[[0,4,8,12]],
                           [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]]
        current_index  = 1 # Note that indexes start at 0
        cur_level      = 1
        abs_states_dic = {4:[(1,0),(0,0)]} # only contains value that will be used
        absolute_state  = s.absolute_state_from_relative(relative_state,
                                                         cur_level, current_index,
                                                         valid_indexes, abs_states_dic)

    def test_calculate_absolute_state_from_relative_two_levels_advantage_states(self):
        s = sp.Sport()
        relative_state       = ('adv',(0,'a',0)) 
        isolated_level_sizes = [2,15]
        total_level_sizes    = [30,15]
        valid_indexes   = [[[0,15]],
                           [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                           [15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]]]
        current_index  = 1 # Note that indexes start at 0
        cur_level      = 1
        abs_states_dic = {15:[(1,0),(0,0)]} # only contains value that will be used
        absolute_state  = s.absolute_state_from_relative(relative_state,
                                                         cur_level, current_index,
                                                         valid_indexes, abs_states_dic)

        assert absolute_state == [(1,0),('adv',(0,'a',0))]
        
    def test_calculate_absolute_state_from_relative_three_levels(self):
        s = sp.Sport()
        relative_state       = (0,0) 
        isolated_level_sizes = [4,3,3]
        total_level_sizes    = [36,9,3]
        valid_indexes = [[[0,9,18,27]],
                         [[0,3,6],[9,12,15],[18,21,24],[27,30,33]],
                         [[0,1,2],[3,4,5],[6,7,8],[9,10,11],[12,13,14],[15,16,17],[18,19,20],[21,22,23],[24,25,26],[27,28,29],[30,31,32],[33,34,35]]]
        current_index  = 3 # Note that indexes start at 0
        cur_level      = 1
        abs_states_dic = {27:[(1,1),(0,0),(0,0)]} # only contains value that will be used
        absolute_state  = s.absolute_state_from_relative(relative_state, cur_level, current_index, valid_indexes, abs_states_dic)

        assert absolute_state == [(1,1),(0,0),(0,0)]

    def test_calculate_all_absolute_states_basic(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=3)
        isolated_level_sizes = [4]
        total_level_sizes    = [4]
        valid_indexes   = [[[0,1,2,3]]]
        absolute_states  = s.calculate_all_absolute_states(valid_indexes, isolated_level_sizes, total_level_sizes)

        assert absolute_states == {0:[(0,0)],1:[(1,0)],2:[(0,1)],3:[(1,1)]}

    def test_calculate_all_absolute_states_best_of(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=3)
        s.add_hierarchy_level(best_of=3)
        isolated_level_sizes = [4,4]
        total_level_sizes    = [16,4]
        valid_indexes   = [[[0,4,8,12]],
                           [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]]
        absolute_states  = s.calculate_all_absolute_states(valid_indexes, isolated_level_sizes, total_level_sizes)

        assert absolute_states == {0:[(0,0),(0,0)],4:[(1,0),(0,0)],8:[(0,1),(0,0)],12:[(1,1),(0,0)],
                                   1:[(0,0),(1,0)],2:[(0,0),(0,1)],3:[(0,0),(1,1)],
                                   5:[(1,0),(1,0)],6:[(1,0),(0,1)],7:[(1,0),(1,1)],
                                   9:[(0,1),(1,0)],10:[(0,1),(0,1)],11:[(0,1),(1,1)],
                                   13:[(1,1),(1,0)],14:[(1,1),(0,1)],15:[(1,1),(1,1)]}

    def test_next_win_state(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=5)
        s.add_hierarchy_level(goal=4)
        self.assert_win_state_equals(state=[(0,0),(0,0)], expected=[(0,0),(1,0)],sport=s)
        self.assert_win_state_equals(state=[(0,0),(1,0)], expected=[(0,0),(2,0)],sport=s)
        self.assert_win_state_equals(state=[(0,0),(3,0)], expected=[(1,0),(0,0)],sport=s)
        self.assert_win_state_equals(state=[(1,0),(3,0)], expected=[(2,0),(0,0)],sport=s)
        self.assert_win_state_equals(state=[(1,1),(3,3)], expected=[(2,1),(0,0)],sport=s)
        self.assert_win_state_equals(state=[(3,3),(3,0)], expected=['win'],sport=s)

    def test_next_win_state_lead(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=5)
        s.add_hierarchy_level(goal=4,lead=3)
        self.assert_win_state_equals(state=[(0,0),('adv',(1,'',0))], expected=[(0,0),('adv',(2,'',0))],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(2,'',0))], expected=[(1,0),(0,0)],sport=s)
        self.assert_win_state_equals(state=[(0,0),(3,3)], expected=[(0,0),('adv',(1,'',0))],sport=s) 
        self.assert_win_state_equals(state=[(0,0),(3,2)], expected=[(0,0),('adv',(2,'',0))],sport=s) 
        self.assert_win_state_equals(state=[(0,0),('adv',(-1,'',0))], expected=[(0,0),(3,3)],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(-2,'',0))], expected=[(0,0),('adv',(-1,'',0))],sport=s)

    def test_next_win_state_number_of_serves(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=3)
        s.add_hierarchy_level(goal=4,lead=2,number_of_serves=2)

        self.assert_win_state_equals(state=[(0,0),(2,3)], expected=[(0,0),('adv',(0,'b',0))],sport=s)

        self.assert_win_state_equals(state=[(0,0),('adv',(0,'a',0))], expected=[(0,0),('adv',(1,'a',1))],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(0,'a',1))], expected=[(0,0),('adv',(1,'b',0))],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(0,'b',0))], expected=[(0,0),('adv',(1,'b',1))],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(0,'b',1))], expected=[(0,0),('adv',(1,'a',0))],sport=s)
        
        self.assert_win_state_equals(state=[(0,0),('adv',(1,'a',0))], expected=[(1,0),(0,0)],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(1,'a',1))], expected=[(1,0),(0,0)],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(1,'b',0))], expected=[(1,0),(0,0)],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(1,'b',1))], expected=[(1,0),(0,0)],sport=s)

        self.assert_win_state_equals(state=[(0,0),('adv',(-1,'a',0))], expected=[(0,0),('adv',(0,'a',1))],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(-1,'a',1))], expected=[(0,0),('adv',(0,'b',0))],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(-1,'b',0))], expected=[(0,0),('adv',(0,'b',1))],sport=s)
        self.assert_win_state_equals(state=[(0,0),('adv',(-1,'b',1))], expected=[(0,0),('adv',(0,'a',0))],sport=s)

        #self.assert_win_state_equals(state=[(0,0),(3,2)], expected=[(0,0),('adv',(1,'a',1))],sport=s)

    def test_next_lose_state_number_of_serves(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=3)
        s.add_hierarchy_level(goal=4,lead=2,number_of_serves=2)

        self.assert_lose_state_equals(state=[(0,0),(3,2)], expected=[(0,0),('adv',(0,'b',0))],sport=s)

        self.assert_lose_state_equals(state=[(0,0),('adv',(0,'a',0))], expected=[(0,0),('adv',(-1,'a',1))],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(0,'a',1))], expected=[(0,0),('adv',(-1,'b',0))],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(0,'b',0))], expected=[(0,0),('adv',(-1,'b',1))],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(0,'b',1))], expected=[(0,0),('adv',(-1,'a',0))],sport=s)
        
        self.assert_lose_state_equals(state=[(0,0),('adv',(1,'a',0))], expected=[(0,0),('adv',(0,'a',1))],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(1,'a',1))], expected=[(0,0),('adv',(0,'b',0))],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(1,'b',0))], expected=[(0,0),('adv',(0,'b',1))],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(1,'b',1))], expected=[(0,0),('adv',(0,'a',0))],sport=s)

        self.assert_lose_state_equals(state=[(0,0),('adv',(-1,'a',0))], expected=[(0,1),(0,0)],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(-1,'a',1))], expected=[(0,1),(0,0)],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(-1,'b',0))], expected=[(0,1),(0,0)],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(-1,'b',1))], expected=[(0,1),(0,0)],sport=s)

         #self.assert_lose_state_equals(state=[(0,0),(2,3)], expected=[(0,0),('adv',(-1,'a',1))],sport=s)

    def test_next_lose_state_lead(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=5)
        s.add_hierarchy_level(goal=4,lead=3)
        self.assert_lose_state_equals(state=[(0,0),('adv',(-1,'',0))], expected=[(0,0),('adv',(-2,'',0))],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(-2,'',0))], expected=[(0,1),(0,0)],sport=s)
        self.assert_lose_state_equals(state=[(0,0),(3,3)], expected=[(0,0),('adv',(-1,'',0))],sport=s) 
        self.assert_lose_state_equals(state=[(0,0),(2,3)], expected=[(0,0),('adv',(-2,'',0))],sport=s) 
        self.assert_lose_state_equals(state=[(0,0),('adv',(1,'',0))], expected=[(0,0),(3,3)],sport=s)
        self.assert_lose_state_equals(state=[(0,0),('adv',(2,'',0))], expected=[(0,0),('adv',(1,'',0))],sport=s)

    def test_next_lose_state(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=5)
        s.add_hierarchy_level(goal=4)
        self.assert_lose_state_equals(state=[(0,0),(0,0)], expected=[(0,0),(0,1)],sport=s)
        self.assert_lose_state_equals(state=[(0,0),(0,1)], expected=[(0,0),(0,2)],sport=s)
        self.assert_lose_state_equals(state=[(0,0),(0,3)], expected=[(0,1),(0,0)],sport=s)
        self.assert_lose_state_equals(state=[(1,0),(0,3)], expected=[(1,1),(0,0)],sport=s)
        self.assert_lose_state_equals(state=[(1,1),(3,3)], expected=[(1,2),(0,0)],sport=s)
        self.assert_lose_state_equals(state=[(3,3),(0,3)], expected=['lose'],sport=s)

    def assert_win_state_equals(self, state=None, expected=None, sport=None):
        assert sport.calculate_next_win_state(state) == expected 

    def assert_lose_state_equals(self, state=None, expected=None, sport=None):
        assert sport.calculate_next_lose_state(state) == expected

    #### Generating transition matrixes ###

    def test_transition_matrix_single_level(self):
        s = sp.Sport()
        s.add_hierarchy_level(goal=3)
        t_m       = s.compute_transition_matrix()
        real_t_m  = self.get_transition_matrix_single_level()
        np.testing.assert_allclose(t_m, real_t_m, atol=1e-1)

    def test_transition_matrix_double_level(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=3)
        s.add_hierarchy_level(goal=2)
        t_m       = s.compute_transition_matrix()
        real_t_m  = self.get_transition_matrix_double_level()
        np.testing.assert_allclose(t_m, real_t_m, atol=1e-1)

    def test_transition_matrix_lead(self):
        s = sp.Sport()
        s.add_hierarchy_level(goal=3, lead=2)
        t_m       = s.compute_transition_matrix()
        real_t_m  = self.get_trans_matrix_lead_2()
        np.testing.assert_allclose(t_m, real_t_m, atol=1e-1)

    def test_transition_matrix_lead_golden(self):
        s = sp.Sport()
        s.add_hierarchy_level(goal=4, lead=2, golden=6)
        t_m       = s.compute_transition_matrix()
        real_t_m  = self.get_trans_matrix_lead_golden()
        np.testing.assert_allclose(t_m, real_t_m, atol=1e-1)

    def test_transition_matrix_lead_golden_multiple_level(self):
        s = sp.Sport()
        s.add_hierarchy_level(best_of=3)
        s.add_hierarchy_level(goal=4, lead=3, golden=5)
        t_m       = s.compute_transition_matrix()
        real_t_m  = self.get_trans_matrix_lead_golden_multiple_level()
        np.testing.assert_allclose(t_m, real_t_m, atol=1e-1)

    def test_transition_matrix_tiebreaker_serve(self):
        s = sp.Sport()
        s.add_hierarchy_level(goal=3, lead=2, number_of_serves=2)
        t_m = s.compute_transition_matrix()
        real_t_m = self.get_transition_matrix_tiebreaker()
        np.testing.assert_allclose(t_m, real_t_m, atol=1e-1)

    def get_transition_matrix_tiebreaker(self):
        win  = 20
        lose = 21
        spw_a, spw_b = 0.7, 0.6
        transition_matrix = np.zeros((20,22))
        transition_matrix[0][1]     = spw_a
        transition_matrix[0][2]     = 1-spw_a
        transition_matrix[1][3]     = 1-spw_b
        transition_matrix[1][4]     = spw_b
        transition_matrix[2][4]     = 1-spw_b
        transition_matrix[2][5]     = spw_b
        transition_matrix[3][win]   = 1-spw_b
        transition_matrix[3][6]     = spw_b
        transition_matrix[4][6]     = 1-spw_b
        transition_matrix[4][7]     = spw_b
        transition_matrix[5][7]     = 1-spw_b
        transition_matrix[5][lose]  = spw_b
        transition_matrix[6][win]   = spw_a
        transition_matrix[6][9]     = 1-spw_a
        transition_matrix[7][9]     = spw_a
        transition_matrix[7][lose]  = 1-spw_a
        transition_matrix[8][13]    = spw_a
        transition_matrix[8][17]    = 1-spw_a
        transition_matrix[9][14]    = spw_a
        transition_matrix[9][18]    = 1-spw_a
        transition_matrix[10][15]   = 1-spw_b
        transition_matrix[10][19]   = spw_b
        transition_matrix[11][12]   = 1-spw_b
        transition_matrix[11][16]   = spw_b
        transition_matrix[12][win]  = spw_a
        transition_matrix[12][9]    = 1-spw_a
        transition_matrix[13][win]  = spw_a
        transition_matrix[13][10]   = 1-spw_a
        transition_matrix[14][win]  = 1-spw_b
        transition_matrix[14][11]   = spw_b
        transition_matrix[15][win]  = 1-spw_b
        transition_matrix[15][8]    = spw_b
        transition_matrix[16][9]    = spw_a
        transition_matrix[16][lose] = 1-spw_a
        transition_matrix[17][10]   = spw_a
        transition_matrix[17][lose] = 1-spw_a
        transition_matrix[18][11]   = 1-spw_b
        transition_matrix[18][lose] = spw_b
        transition_matrix[19][8]    = 1-spw_b
        transition_matrix[19][lose] = spw_b
        return transition_matrix

    def get_transition_matrix_single_level(self):
        win = 9
        lose = 10
        wp, lp = 1,-1
        transition_matrix = np.zeros((9,11))
        transition_matrix[0][1] = wp
        transition_matrix[0][2] = lp
        transition_matrix[1][3] = wp
        transition_matrix[1][4] = lp
        transition_matrix[2][4] = wp
        transition_matrix[2][5] = lp
        transition_matrix[3][win] = wp
        transition_matrix[3][6] = lp
        transition_matrix[4][6] = wp
        transition_matrix[4][7] = lp
        transition_matrix[5][7] = wp
        transition_matrix[5][lose] = lp
        transition_matrix[6][win] = wp
        transition_matrix[6][8] = lp
        transition_matrix[7][8] = wp
        transition_matrix[7][lose] = lp
        transition_matrix[8][win] = wp
        transition_matrix[8][lose] = lp
        return transition_matrix

    def get_transition_matrix_double_level(self):
        win = 16
        lose = 17
        wp, lp = 1,-1
        transition_matrix = np.zeros((16,18))
        transition_matrix[0][1] = wp
        transition_matrix[0][2] = lp
        transition_matrix[1][4] = wp
        transition_matrix[1][3] = lp
        transition_matrix[2][3] = wp
        transition_matrix[2][8] = lp
        transition_matrix[3][4] = wp
        transition_matrix[3][8] = lp
        transition_matrix[4][5] = wp
        transition_matrix[4][6] = lp
        transition_matrix[5][win] = wp
        transition_matrix[5][7] = lp
        transition_matrix[6][7] = wp
        transition_matrix[6][12] = lp
        transition_matrix[7][win] = wp
        transition_matrix[7][12] = lp
        transition_matrix[8][9] = wp
        transition_matrix[8][10] = lp
        transition_matrix[9][12] = wp
        transition_matrix[9][11] = lp
        transition_matrix[10][11] = wp
        transition_matrix[10][lose] = lp
        transition_matrix[11][12] = wp
        transition_matrix[11][lose] = lp
        transition_matrix[12][13] = wp
        transition_matrix[12][14] = lp
        transition_matrix[13][win] = wp
        transition_matrix[13][15] = lp
        transition_matrix[14][15] = wp
        transition_matrix[14][lose] = lp
        transition_matrix[15][win] = wp
        transition_matrix[15][lose] = lp
        return transition_matrix

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

    def get_trans_matrix_lead_2(self):
        # goal=3, lead=2
        win_index = 11
        lose_index = 12
        wp = 1
        lp = -1
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
    
    def get_trans_matrix_lead_golden(self):
        # goal = 4, lead= 2, golden = 6
        win_index = 22
        lose_index = 23
        trans_m = np.zeros((22,24))
        wp = 1
        lp = -1

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
    #### Running simulations ###

    def get_trans_matrix_lead_golden_multiple_level(self):
        # best_of = 4
        # goal = 4, lead= 3, golden = 5
        win_index = 84
        lose_index = 85
        trans_m = np.zeros((84,86))
        wp = 1
        lp = -1
    
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
        trans_m[6][21] = wp
        trans_m[6][10] = lp
        trans_m[7][10] = wp
        trans_m[7][11] = lp
        trans_m[8][11] = wp
        trans_m[8][12] = lp
        trans_m[9][12] = wp
        trans_m[9][42] = lp
        trans_m[10][21] = wp
        trans_m[10][13] = lp
        trans_m[11][13] = wp
        trans_m[11][14] = lp
        trans_m[12][14] = wp
        trans_m[12][42] = lp
        trans_m[13][15] = wp
        trans_m[13][16] = lp
        trans_m[14][16] = wp
        trans_m[14][17] = lp
        trans_m[15][21] = wp
        trans_m[15][18] = lp
        trans_m[16][18] = wp
        trans_m[16][19] = lp
        trans_m[17][19] = wp
        trans_m[17][42] = lp
        trans_m[18][21] = wp
        trans_m[18][20] = lp
        trans_m[19][20] = wp
        trans_m[19][42] = lp
        trans_m[20][21] = wp
        trans_m[20][42] = lp

        trans_m[21][22] = wp
        trans_m[21][23] = lp
        trans_m[22][24] = wp
        trans_m[22][25] = lp
        trans_m[23][25] = wp
        trans_m[23][26] = lp
        trans_m[24][27] = wp
        trans_m[24][28] = lp
        trans_m[25][28] = wp
        trans_m[25][29] = lp
        trans_m[26][29] = wp
        trans_m[26][30] = lp
        trans_m[27][win_index] = wp
        trans_m[27][31] = lp
        trans_m[28][31] = wp
        trans_m[28][32] = lp
        trans_m[29][32] = wp
        trans_m[29][33] = lp
        trans_m[30][33] = wp
        trans_m[30][63] = lp
        trans_m[31][win_index] = wp
        trans_m[31][34] = lp
        trans_m[32][34] = wp
        trans_m[32][35] = lp
        trans_m[33][35] = wp
        trans_m[33][63] = lp
        trans_m[34][36] = wp
        trans_m[34][37] = lp
        trans_m[35][37] = wp
        trans_m[35][38] = lp
        trans_m[36][win_index] = wp
        trans_m[36][39] = lp
        trans_m[37][39] = wp
        trans_m[37][40] = lp
        trans_m[38][40] = wp
        trans_m[38][63] = lp
        trans_m[39][win_index] = wp
        trans_m[39][41] = lp
        trans_m[40][41] = wp
        trans_m[40][63] = lp
        trans_m[41][win_index] = wp
        trans_m[41][63] = lp
        
        trans_m[42][43] = wp
        trans_m[42][44] = lp
        trans_m[43][45] = wp
        trans_m[43][46] = lp
        trans_m[44][46] = wp
        trans_m[44][47] = lp
        trans_m[45][48] = wp
        trans_m[45][49] = lp
        trans_m[46][49] = wp
        trans_m[46][50] = lp
        trans_m[47][50] = wp
        trans_m[47][51] = lp
        trans_m[48][63] = wp
        trans_m[48][52] = lp
        trans_m[49][52] = wp
        trans_m[49][53] = lp
        trans_m[50][53] = wp
        trans_m[50][54] = lp
        trans_m[51][54] = wp
        trans_m[51][lose_index] = lp
        trans_m[52][63] = wp
        trans_m[52][55] = lp
        trans_m[53][55] = wp
        trans_m[53][56] = lp
        trans_m[54][56] = wp
        trans_m[54][lose_index] = lp
        trans_m[55][57] = wp
        trans_m[55][58] = lp
        trans_m[56][58] = wp
        trans_m[56][59] = lp
        trans_m[57][63] = wp
        trans_m[57][60] = lp
        trans_m[58][60] = wp
        trans_m[58][61] = lp
        trans_m[59][61] = wp
        trans_m[59][lose_index] = lp
        trans_m[60][63] = wp
        trans_m[60][62] = lp
        trans_m[61][62] = wp
        trans_m[61][lose_index] = lp
        trans_m[62][63] = wp
        trans_m[62][lose_index] = lp

        trans_m[63][64] = wp
        trans_m[63][65] = lp
        trans_m[64][66] = wp
        trans_m[64][67] = lp
        trans_m[65][67] = wp
        trans_m[65][68] = lp
        trans_m[66][69] = wp
        trans_m[66][70] = lp
        trans_m[67][70] = wp
        trans_m[67][71] = lp
        trans_m[68][71] = wp
        trans_m[68][72] = lp
        trans_m[69][win_index] = wp
        trans_m[69][73] = lp
        trans_m[70][73] = wp
        trans_m[70][74] = lp
        trans_m[71][74] = wp
        trans_m[71][75] = lp
        trans_m[72][75] = wp
        trans_m[72][lose_index] = lp
        trans_m[73][win_index] = wp
        trans_m[73][76] = lp
        trans_m[74][76] = wp
        trans_m[74][77] = lp
        trans_m[75][77] = wp
        trans_m[75][lose_index] = lp
        trans_m[76][78] = wp
        trans_m[76][79] = lp
        trans_m[77][79] = wp
        trans_m[77][80] = lp
        trans_m[78][win_index] = wp
        trans_m[78][81] = lp
        trans_m[79][81] = wp
        trans_m[79][82] = lp
        trans_m[80][82] = wp
        trans_m[80][lose_index] = lp
        trans_m[81][win_index] = wp
        trans_m[81][83] = lp
        trans_m[82][83] = wp
        trans_m[82][lose_index] = lp
        trans_m[83][win_index] = wp
        trans_m[83][lose_index] = lp
        return trans_m
