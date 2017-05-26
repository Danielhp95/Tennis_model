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

    #### Generating transition matrixes ###

    #### Running simulations ###



