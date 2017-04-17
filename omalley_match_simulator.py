from omalley import omalley
from dataLoggers import matchLogger as ml
import numpy as np

# Sample from a normal using mean and variance from each player for 
# each simulation.

# Use fixed mean and variance from each player.
def simulate_match(mean_a, mean_b, variance_a, variance_b):
    logger = ml.matchLogger("Omalley cnst", "M3", "None")
    score = [0,0] # Player's score
    player_a_serves = True
    while not is_match_over(score):
        game_score = [0,0]
        while not is_set_over(game_score):
            p = None
            serve_p_a = mean_a
            serve_p_b = mean_b
            if is_TB_game(game_score):
                p = omalley.TB(mean_a, mean_b)
            else:
                p = omalley.G(serve_p_a) if player_a_serves else omalley.G(1-serve_p_b)

            u = np.random.uniform(0,1)
            game_score[0] += 1 if u <= p else 0
            game_score[1] += 1 if u > p else 0

            # Change of serve
            player_a_serves = not player_a_serves
        # Set finishes, update score 
        winner = update_set_score(game_score, score)
        ml.logSet(winner, game_score)
    return score


# Technical debt: check form M3 AND M5
def is_match_over(score):
    return score[0] >= 3 or score[1] >= 3

# Technical debt: take into account different tournaments
def is_set_over(game_score):
    # Normal win
    is_over   = game_score[0] == 6 and game_score[1] <= 4
    is_over_2 = game_score[1] == 6 and game_score[0] <= 4
    # Tiebreak win
    is_over_3 = game_score[0] == 7 or game_score[1] == 7 
    return is_over or is_over_2 or is_over_3 

def is_TB_game(game_score):
    return game_score[0] == 6 and game_score[1] == 6

def update_game_score(logger, score):
    return

def update_set_score(logger, game_score, score):
    winner = None
    if game_score[0] > game_score[1]:
        winner = 0
        score[0] += 1
    else:
        winner = 1
        score[1] += 1
    return winner
