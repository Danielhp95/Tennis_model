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

    def assert_game_level_size(self,goal=0, lead=0, golden=float('inf'),
                               best_of=None, expected_size=-1):
        s = sp.Sport()
        size = s.calculate_number_of_states(goal, lead, golden, best_of)
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
        absolute_state  = s.absolute_state_from_relative(relative_state, cur_level, current_index, valid_indexes, abs_states_dic)

        assert absolute_state == [(1,0),(0,1)]
        
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

    def test_calculate_all_absolute_states_(self):
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

    #def test_win_index_from_valid_indexes(self):
    #    s = sp.Sport()
    #    isolated_level_sizes = [4,3,3]
    #    total_level_sizes    = [36,9,3]
    #    valid_indexes = [[[0,9,18,27]],
    #                     [[0,3,6],[9,12,15],[18,21,24],[27,30,33]],
    #                     [[0,1,2],[3,4,5],[6,7,8],[9,10,11],[12,13,14],[15,16,17],[18,19,20],[21,22,23],[24,25,26],[27,28,29],[30,31,32],[33,34,35]]]

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
        iso = sport.isolated_level_size()
        tot = sport.aggregated_level_size(iso)
        valid_indexes = sport.generate_all_valid_indexes(iso, tot)
        abs_index_to_states = sport.calculate_all_absolute_states(valid_indexes, iso, tot)
        assert expected == sport.calculate_next_win_state(state)

    def assert_lose_state_equals(self, state=None, expected=None, sport=None):
        iso = sport.isolated_level_size()
        tot = sport.aggregated_level_size(iso)
        valid_indexes = sport.generate_all_valid_indexes(iso, tot)
        abs_index_to_states = sport.calculate_all_absolute_states(valid_indexes, iso, tot)
        assert expected == sport.calculate_next_lose_state(state)

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

    #### Running simulations ###
