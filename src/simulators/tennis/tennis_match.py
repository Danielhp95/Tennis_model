from __future__ import division
import math
from tennis_set import Set

class Match(object):

    #TODO: include ser win probability calculator
    def __init__(self, spw, best_of, tiebreaker_final_set):
        self.spw                  = spw
        self.best_of              = best_of
        self.tiebreaker_final_set = tiebreaker_final_set
        self.tiebreaker           = False

        self.sets_won    = [0,0]
        self.sets_to_win = math.ceil(best_of / 2)

        self.sets_played      = []

        self.total_serves     = [0,0]
        self.total_serves_won = [0,0]

        self.server = 0

    def play(self):
        while not self.is_over():
            is_final_set = (self.sets_won[0] == self.sets_to_win - 1) and \
                    (self.sets_won[1] == self.sets_to_win - 1)

            current_set = Set(self, self.final_set, self.tiebreaker_final_set,
                              self.spw)

            set_winner  =  current_set.play()
            self.sets_won[set_winner] += 1 

            self.sets_played.append(current_set)
        
        return self.get_winner()

    def is_over(self):
        player_a_won = self.sets_won[0] == self.sets_to_win
        player_b_won = self.sets_won[1] == self.sets_to_win
        return player_a_won or player_b_won

    def get_winner(self):
        if self.sets_won[0] == self.sets_to_win:
            return 0
        elif self.sets_won[1] == self.sets_to_win:
            return 1

    def sets_played(self):
        return sum(self.sets_won)

    def set_tiebreaker(self):
        self.tiebreaker = True

    def switch_server(self):
        self.server = 0 if self.server == 1 else 1

    def get_server(self):
        return self.server

    def increase_serves(self, server, result):
        self.total_serves[server] += 1
        if result:
            self.total_serves_won[server] += 1

