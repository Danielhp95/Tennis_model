
class FiftyFiftyModel(object):

    def calculate_odds(self, player_a, player_b, matches_up_to_date):
        return 1.0

class AlternatePlayerModel(object):

    def __init__(self):
        self.oddity = 0

    def calculate_odds(self, player_a, player_b, matches_up_to_date):
        odds = 1.0 if self.oddity == 1 else 0.0
        self.oddity = (self.oddity + 1) % 2
        return 1.0


