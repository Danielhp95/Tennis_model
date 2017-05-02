import match_simulator as simulator
import numpy as np

def normal(mean_a, var_a, mean_b, var_b, game_score, match_score, *args):
    return np.random.normal(mean_a, var_a)

sim = simulator.MatchSimulator(best_of=3)
sim.serve_probability_f = normal
print(sim.simulate_match(0.5,0.5,0,0))
