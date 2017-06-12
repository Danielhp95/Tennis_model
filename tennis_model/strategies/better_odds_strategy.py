
# A strategy always returns the amount of money being bet on the match
"""
    Strategy documentation
"""

class BetIfBetterOddsForPredictedWinnerStrategy(object):

    def strategy(self, model_odds_player_a, model_odds_player_b,
                 average_betting_exchange_odds_a, average_betting_exchange_odds_b,
                 *args):
        if model_odds_player_a >= model_odds_player_b:
            if average_betting_exchange_odds_a > model_odds_player_a:
                return 1,'a'
        else:
            if average_betting_exchange_odds_b > model_odds_player_b:
                return 1,'b'
        return 0, 'a'
