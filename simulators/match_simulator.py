import os, sys
project_path = os.path.abspath(os.path.join('..'))
sys.path.append(project_path)
from omalley import omalley
from dataLoggers import matchLogger as ml
import numpy as np

class MatchSimulator(object):

    """
    Params:
        best_of     -> Represents best of 5 or best of 3 match
        game_f      -> function that determines prob of player winning a game
        tie_break_b -> function that determines prob of player winning a tie_break 
        set_f       -> function that determines prob of player winning a set 
        serv_probability_f -> function that determines prob of player winning a serve
                       Initial parameters are fixed. Custom parameters can be added
                       at the end and retrived in *custom_args
    """
    def __init__(self, best_of=5, game_f=omalley.G, tie_break_game_f=omalley.TB, set_f=omalley.S, serv_probability_f=None):
        assert(best_of == 3 or best_of == 5)
        self.best_of          = best_of

        self.game_f           = game_f
        self.tie_break_game_f = tie_break_game_f
        self.set_f            = set_f

        # If no serve probability function is passed, identity is used
        if serv_probability_f == None:
            self.serv_probability_f = lambda player_mean, player_var, opponent_mean, opponent_var, game_score, match_score, *custom_args: player_mean

    # Use fixed mean and variance from each player.
    def simulate_match(self, mean_a, mean_b, var_a, var_b):
        logger          = ml.matchLogger("Omalley cnst", "M3", "None")
        match_score     = [0,0]
        player_a_serves = True

        while not self.is_match_over(match_score):
            game_score = [0,0]
            while not self.is_set_over(game_score):
                p = None

                serve_p_a = self.serv_probability_f(mean_a, var_a, mean_b, var_b, game_score, match_score)
                serve_p_b = self.serv_probability_f(mean_b, var_b, mean_a, var_a, game_score, match_score)

                if self.is_TB_game(game_score):
                    p = self.tie_break_game_f(mean_a, mean_b)
                else:
                    p = self.game_f(serve_p_a) if player_a_serves else omalley.G(1-serve_p_b)

                game_winner = self.update_game_score(p, game_score)
                player_a_serves = not player_a_serves # Change of serve

            # Set finishes, update score 
            set_winner = self.update_set_score(game_score, match_score)
            logger.logSet(set_winner, game_score)

        match_winner = 'a' if match_score[0] > match_score[1] else 'b'
        logger.logMatch(match_winner, match_score)
        print(logger)
        return match_score

    # Technical debt: check form M3 AND M5
    def is_match_over(self, score):
        if self.best_of == 5:
            return score[0] >= 3 or score[1] >= 3
        elif self.best_of == 3:
            return score[0] >= 2 or score[1] >= 2

    # Technical debt: take into account different tournaments
    def is_set_over(self, game_score):
        # Normal win
        is_over   = game_score[0] == 6 and game_score[1] <= 4
        is_over_2 = game_score[1] == 6 and game_score[0] <= 4
        # Tiebreak win
        is_over_3 = game_score[0] == 7 or game_score[1] == 7 
        return is_over or is_over_2 or is_over_3 

    def is_TB_game(self, game_score):
        return game_score[0] == 6 and game_score[1] == 6

    # Might wanna add probability as a meassure
    def update_game_score(self, p, game_score):
        winner = None
        u = np.random.uniform(0,1)
        if u <= p:
            winner = 0
            game_score[0] += 1
        elif u > p:
            winner = 1
            game_score[1] += 1
        return winner

    def update_set_score(self, game_score, score):
        winner = None
        if game_score[0] > game_score[1]:
            winner = 0
            score[0] += 1
        else:
            winner = 1
            score[1] += 1
        return winner
