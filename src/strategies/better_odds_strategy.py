
# A strategy always returns the amount of money being bet on the match
def strategy(model_odds_player_a, model_odds_player_b, average_betting_exchange_odds_a, average_betting_exchange_odds_b, bet=1):
    odds_difference_a = model_odds_player_a - average_betting_exchange_odds_a
    odds_difference_b = model_odds_player_b - average_betting_exchange_odds_b
  
    if odds_difference_a > 0 and odds_difference_a > odds_difference_b:
        return bet, 'a'
    elif odds_difference_b > 0 and odds_difference_b > odds_difference_b:
        return bet, 'b'
    else:
        return 0
