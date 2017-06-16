
class BetOnLoserStrategy(object):

    def strategy(self,*args):
       '''
       Always bets 1 token monney to the loser, which is the player 'b'
       '''
       return 1, 'b'

class BetOnWinnerStrategy(object):

    def strategy(self,model_odds_player_a, model_odds_player_b,
                 average_betting_exchange_odds_a, average_betting_exchange_odds_b,
                 *args):

        return 1, 'a'

class RecordDatesStrategy(object):

    def __init__(self):
        self.dates = []

    def strategy(self,model_odds_player_a, model_odds_player_b,
                 average_betting_exchange_odds_a, average_betting_exchange_odds_b,
                 match):

        assert all(map(lambda date: date <= match['Date'], self.dates)) 
        self.dates.append(match['Date'])
        return 0, 'a'

class BetIfBetterOddsForPredictedWinner(object):

    def strategy(*args):
        model_predicted_winner_odds = 0
        bet_exchange_predicted_winner_odds = 0
        if bet_exchange_predicted_winner_odds > model_predicted_winner_odds:
            return 1,'a'
        else:
            return 0, '0'

class KellyCriterion(object):

    def strategy(*args):
        # Calculate things below from argumets
        average_winning_odds = 0
        winnin_prob          = 0
        losing_prob          = 1 - winnin_prob
        bet = (winnin_prob*(average_winning_odds + 1) - 1)/average_winning_odds
    
class AlternateBettingStrategy(object):
    
    def __init__(self):
        self.oddity = 0

    def strategy(*args):
        choice = 'a' if self.oddity == 1 else 'b'
        self.oddity = (self.oddity + 1) % 2
        bet = 10**(-6)
        return bet, choice

class NeverBetStrategy(object):

    def strategy(*args):
        return 0, 'b'
