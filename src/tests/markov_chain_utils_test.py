import unittest
import os, sys
markov_path = os.path.abspath(os.path.join('..','simulators','markov_chains'))
sys.path.append(markov_path)
import numpy as np

import markov_chain_utils as mcu


class MarkovChainTest(unittest.TestCase):

    def test_drunkard_walk_probabilities(self):
        Q = np.array([[0.0,0.5,0.0],[0.5,0.0,0.5],[0.0,0.5,0.0]])
        R = np.array([[0.5,0.0],[0.0,0.0],[0.0,0.5]])
        I = np.eye(3,3)
        real_B = np.array([[0.75, 0.25],[0.5,0.5],[0.25,0.75]])

        calculated_B = mcu.calculate_absorption_probabilities(Q,I,R)
        np.testing.assert_allclose(real_B, calculated_B, rtol=1e-1)

