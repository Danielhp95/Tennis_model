from omalley import omalley
import numpy as np

# Sample from a normal using mean and variance from each player for 
# each simulation.

# Use fixed mean and variance from each player.
def simulate_match(winning_probability):
    u = numpy.random.uniform(0,1)
    return 1 if u <= winning_probability else 0

def batch_simulations(num_simulations, mean_a, mean_b,
                      variance_a, variance_b):
    
    for i in range(0,num_simulations):
        winning_probability = omalley.M3(mean_a, mean_b)
        outcome = simulate_match(winning_probability)
        if outcome == 1: # player A win
            #do something
        elif outcome == 0: # player A loss
            #do something


