from omalley import omalley
import numpy as np

# Sample from a normal using mean and variance from each player for 
# each simulation.

# Use fixed mean and variance from each player.
def simulate_match(mean_a, mean_b, variance_a, variance_b):
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
                p = omalley.G(serve_p_a) if player_a_serves else omalley.G(serve_p_b)

            u = np.random.uniform(0,1)
            score[0] += 1 if u <= p else 0
            score[1] += 1 if u > p else 0

            # Change of serve
            player_a_serves = not player_a_serves
        if game_score[0] > game_score[1]:
            score[0] += 1
        else:
            score[1] += 1
    return score




def is_match_over(score):
    return False

def is_set_over(game_score):
    return False

def is_TB_game(game_score):
    return False

def batch_simulations(num_simulations, mean_a, mean_b,
                      variance_a, variance_b):
    
    for i in range(0,num_simulations):
        winning_probability = omalley.M3(mean_a, mean_b)
        outcome = simulate_match(winning_probability)
        if outcome == 1: # player A win
            #do something
        elif outcome == 0: # player A loss
            #do something
    return None

