from __future__ import division
import tennis_model
from tennis_model.simulators.tennis import tennis_match
import pandas as pd
import math

class SimulationModel(object):

    def __init__(self, simulations=1000):
        self.simulations = simulations

    def is_safe_datapoint(self, *vals):
        any_nan = any(map(math.isnan, vals))
        any_none = any(map(lambda x: x is None, vals))
        return not any_nan and not any_none

    def find_average_spw(self, p, matches):
        serves = 0
        serves_won = 0
        for i, r in matches.iterrows():
            if p == r['Winner'] and self.is_safe_datapoint(r['w_svpt'],r['w_1stWon'],r['w_2ndWon']):
                serves += r['w_svpt']
                serves_won += r['w_1stWon'] + r['w_2ndWon']
            elif p == r['Loser'] and self.is_safe_datapoint(r['l_svpt'],r['l_1stWon'],r['l_2ndWon']):
                serves += r['l_svpt']
                serves_won += r['l_1stWon'] + r['l_2ndWon']

        if serves == 0 or math.isnan(serves):
            print('Didnt match player with player: ' + p)
            serves = 100
            serves_won = 65

        return serves_won / serves

    def calculate_odds(self, player_a, player_b, matches_up_to_date):
        spw_a = self.find_average_spw(player_a, matches_up_to_date)
        spw_b = self.find_average_spw(player_b, matches_up_to_date)
        print('spw_a: ' + str(spw_a))
        print('spw_b: ' + str(spw_b))

        wins = [0,0]
        for i in range(0, self.simulations):
            match = tennis_match.Match([spw_a, spw_b], 5,False)
            winner = match.play()
            wins[winner] += 1
        print(wins)
        wins_percentage = map(lambda x: x/self.simulations, wins)
        if wins_percentage[0] == 0:
            wins_percentage[0] = 1
        print('win percentage a: ' + str(wins_percentage[0]))
        return 1.0/wins_percentage[0]
