import unittest
import os, sys
sim_path = os.path.abspath(os.path.join('..',))
sys.path.append(sim_path)
from simulators.tennis import tennis_match, tennis_set, tennis_game
import pandas as pd

class TennisSimulatorTest(unittest.TestCase):

    ### Tests for Game class ###
    def test_game_minimum_amount_of_points(self):
        spw = [1.0,0.0]
        m = tennis_match.Match(spw, 3, False)
        g = tennis_game.Game(m,spw, False)
        winner = g.play()
        assert g.points_won[0] == 4
        assert g.points_won[1] == 0
        assert g.points_played() == 4
        assert winner == 0
        assert g.points_to_win == 4

    def test_game_has_player_won(self):
        m = tennis_match.Match(None, 3, False)
        g = tennis_game.Game(m,None, False)
        g.points_won = [6,4]
        assert g.player_won(1) == False
        assert g.player_won(0) == True

    def test_game_tiebreak_rules(self):
        spw = [1.0,0.0]
        tiebreak = True
        m = tennis_match.Match(spw, 3, False)
        g = tennis_game.Game(m,spw, tiebreak)
        winner = g.play()
        assert winner == 0
        assert g.points_won[0] == 6
        assert g.points_won[1] == 0
        assert g.points_to_win == 6


    def test_game_tiebreak_switches_server(self):
        spw = [1.0,0.0]
        tiebreak = True
        m = tennis_match.Match(spw, 3, False)
        g = tennis_game.Game(m,spw, tiebreak)
        winner = g.play()

        assert m.total_serves == [3,3]
        assert g.points_won   == [6,0]

    ### Tests for Set class ###
    def test_set_min_amount_of_games(self):
        spw = [1.0, 0.0]
        m = tennis_match.Match(spw, 3, False)
        s = tennis_set.Set(m,False,False,spw)
        winner = s.play()
        assert winner == 0
        assert s.games_won == [6,0]
        assert len(s.games_played) == 6

    def test_set_player_b_wins(self):
        spw = [0.0, 1.0]
        m = tennis_match.Match(spw, 3, False)
        s = tennis_set.Set(m,False,False,spw)
        winner = s.play()
        assert winner == 1
        assert s.games_won == [0,6]

    def test_set_tiebreaker_is_set_on_match(self):
        spw = [0.0, 1.0]
        m = tennis_match.Match(spw, 3, False)
        s = tennis_set.Set(m,False,False,spw)
        s.games_won = [6,6]
        winner = s.play()
        assert m.tiebreaker == True

    ### Tests for Match class ###

    def test_match_min_amount_of_sets_best_of_3(self):
        spw = [1.0, 0.0]
        m = tennis_match.Match(spw,3, False)
        winner = m.play()
        assert winner == 0
        assert m.sets_won == [2,0]
        assert m.total_serves_won == [24,0]
        assert m.total_serves == [24,24]

    def test_match_min_amount_of_sets_best_of_5(self):
        spw = [1.0, 0.0]
        m = tennis_match.Match(spw,5, False)
        winner = m.play()
        assert winner == 0
        assert m.sets_won == [3,0]
        assert m.total_serves_won == [36,0]
        assert m.total_serves == [36,36]

    def test_match_min_player_b_wins(self):
        spw = [0.0, 1.0]
        m = tennis_match.Match(spw,5, False)
        winner = m.play()
        assert winner == 1
        assert m.sets_won == [0,3]
        assert m.total_serves_won == [0,36]
        assert m.total_serves == [36,36]

    def test_match_tiebreaker_final_set(self):
        spw = [0.0,1.0]
        tiebreaker_final_set = True
        m = tennis_match.Match(spw, 5, tiebreaker_final_set)
        winner = m.play()
        assert m.tiebreaker_final_set == True
        assert winner == 1
        assert m.sets_won == [0,3]
        assert m.total_serves_won == [0.0,36.0]

    def test_match_switch_server(self):
        m = tennis_match.Match([0,0], 3, False)
        m.switch_server()
        assert m.get_server() == 1
        m.switch_server()
        assert m.get_server() == 0
        m.switch_server()
        assert m.get_server() == 1

    ### Tests for STATISTICS ###

#   def test_statistics_median_game_length(self):
#       assert False

#   def tsst_statistics_average_game_length(self):
#       assert False

#   def test_statistics_win_game_probability(self):
#       assert False

#   def test_statistics_win_set_probability(self):
#       assert False

#   def test_statistics_win_match_probability(self):
#       assert False

#   def test_statistics_serve_win_probability_both_players(self):
#       assert False
