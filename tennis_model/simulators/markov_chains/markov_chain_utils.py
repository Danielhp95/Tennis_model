import numpy as np


'''
    The matrix should be t x 2, where t is the number of transient states
    in the markov chain. 2 is the number of absorbing states. for any t, tx1
    is the probability of starting in state t and winning the match. tx2
    is the same, but losing the match.
'''
def calculate_absorption_probabilities(Q,I,R):
    N = np.linalg.inv(I - Q)
    return np.dot(N,R)
