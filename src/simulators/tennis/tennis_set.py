from tennis_game import Game

class Set(object):

    def __init__(self, match, final_set, tiebreaker_final_set, spw):
        self.match                = match
        self.final_set            = final_set
        self.tiebreaker_final_set = tiebreaker_final_set

        self.spw = spw

        self.games_won = [0,0]
        self.games_played = []

    def play(self):
        while not self.is_over():
            tiebreak = (not self.final_set or self.tiebreaker_final_set) and \
                        self.games_won[0] == 6 and self.games_won[1] == 6

            # why is tiebreaker set? what does it mean?
            if tiebreak:
                self.match.set_tiebreaker() #See how this can be improved

            current_game = Game(self.match, self.spw, tiebreak)
            game_winner  = current_game.play()

            self.games_won[game_winner] += 1
            self.games_played.append(current_game)

        return self.get_winner()

    def is_over(self):
        player_a_won = self.player_won(0)
        player_b_won = self.player_won(1)
        return player_a_won or player_b_won

    def player_won(self, player):
        opponent = 0 if player else 1

        if not self.final_set or self.tiebreaker_final_set: 
            return (self.games_won[player] >= 6 and  
                    self.games_won[opponent] < 5) or \
                    (self.games_won[player] == 7 and 
                    self.games_won[opponent] <= 6)
        else:
            return self.games_won[player] >= 6 and \
                    self.games_won[opponent] < self.games_won[player] - 1

    # At this point, a player must have won the set
    def get_winner(self):
        return 1 if self.player_won(1) else 0

    def games_played(self):
        return sum(self.games_won)
