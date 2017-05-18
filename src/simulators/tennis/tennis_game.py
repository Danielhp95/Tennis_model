import numpy

class Game(object):

    def __init__(self, match, spw, tiebreak):
        self.match    = match
        self.spw      = spw
        self.tiebreak = tiebreak # might not be necessary

        self.points_to_win = 4 if not tiebreak else 6
        self.points_won    = [0,0]

    def play(self):

        while not self.is_over():
            server   = self.match.get_server()
            reciever = 0 if server == 1 else 1

            u = numpy.random.uniform(low=0.0,high=1.0) 
            result = u < self.spw[server]

            self.match.increase_serves(server, result)
            if result:
                self.points_won[server] += 1
            else:
                self.points_won[reciever] += 1

            # On tiebreak games, server changes on every served
            if self.tiebreak and self.points_played() % 2 == 1:
                self.match.switch_server()

        self.match.switch_server()
        return self.get_winner()


    def is_over(self):
        player_a_won = self.player_won(0)
        player_b_won = self.player_won(1)
        return player_a_won or player_b_won

    # At this point, a player must have won the point
    def get_winner(self):
        return 1 if self.player_won(1) else 0

    def player_won(self, player):
        opponent = 0 if player == 1 else 1
        return self.points_won[player] >= self.points_to_win and \
                self.points_won[opponent] < (self.points_won[player] - 1)

    def points_played(self):
        return sum(self.points_won)

