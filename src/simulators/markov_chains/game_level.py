from __future__ import division
import numpy as np
import math

class GameLevel:



    def __init__(self, goal=None, lead=0, golden=float("inf"), best_of=None):
        self.wp      = 9999 # will need to turn this into variables
        self.lp      = -9999
        self.goal    = goal
        self.best_of = best_of
        # if there is a best_of, there can not be any lead or golden point,
        # because the game will end after finishing (best_of / 2) games
        if best_of is not None:
            self.golden = float('inf')
            self.lead   = None
        else:
            self.lead   = lead
            self.golden = golden
        self.index_to_state = {}
        self.state_to_index = {}



    '''
        At this point in time, the transition matrix {matrix} has been initiated.
        This function populates a part of the {matrix} using the {valid_indexes}.

        There will be {number_of_transient_states} state additions.
        All winning transitions will point to {win_index}
        All losing transitions will point to {lose_index}
    '''
    def populate_transition_matrix(self, matrix, number_of_transient_states, valid_indexes,
            win_index, lose_index):
        # Initialize state population
        initial_index          = valid_indexes[0]
        self.states_populated  = {initial_index : (0,0)}
        self.index_connections = {}

        # Indexes outside current game level
        self.win_index  = win_index
        self.lose_index = lose_index

        # if lead advantage is set and golden point is not set, start by populating adv states
        if self.golden == float('inf') and self.lead > 0:
            adv_states        = valid_indexes[self.goal**2:]
            valid_indexes     = valid_indexes[:self.goal**2]
            advantage = 1
            assert len(adv_states) % 2 == 0
            while len(adv_states) > 0:
                a_adv, b_adv = adv_states.pop(0), adv_states.pop(0)
                a_win_index, a_lose_index = a_adv + 2, a_adv - 2
                b_win_index, b_lose_index = b_adv - 2, b_adv + 2
                if advantage == 1:
                    a_lose_index = a_adv - 1
                if advantage == self.lead - 1:
                    a_win_index  = win_index
                    b_lose_index = lose_index
                matrix[a_adv][a_win_index]  = self.wp
                matrix[a_adv][a_lose_index] = self.lp
                matrix[b_adv][b_win_index]  = self.wp
                matrix[b_adv][b_lose_index] = self.lp

                self.states_populated[a_adv] = ('adv', advantage)
                self.states_populated[('adv',advantage)]  = a_adv
                self.states_populated[b_adv] = ('adv', -advantage)
                self.states_populated[('adv',-advantage)] = b_adv
                self.index_connections[a_adv] = (a_win_index, a_lose_index)
                self.index_connections[b_adv] = (b_win_index, b_lose_index)

        # Create a copy of indexes to use whilst traversing
        available_indexes = valid_indexes[1:]

        # Use iterator for valid indexes 
        for i in valid_indexes:
            s_a ,s_b = self.states_populated[i]

            print(str(s_a) + ', ' + str(s_b))
            outcome_a = self.is_over((s_a + 1, s_b), self.goal, self.lead, self.golden, self.best_of)
            outcome_b = self.is_over((s_a    , s_b + 1), self.goal, self.lead, self.golden, self.best_of)

            self.index_connections[i] = (win_index, lose_index)

        # The part of the matrix corresponding to this part of the game must be filled by now
        # There must be no available indexes left
        assert len(available_indexes) == 0

    def calculate_states_from_indexes(self, number_of_transient_states, valid_indexes):
        # Initialize state population
        initial_index = valid_indexes[0]
        initial_state = (0,0)
        self.index_to_state[initial_index] = (0,0)
        self.state_to_index[initial_state] = initial_index

        if self.golden == float('inf') and self.lead > 0:
            valid_indexes = self.add_lead_indexes(valid_indexes,)

        available_indexes = valid_indexes[1:]
        for i in valid_indexes:
            s_a ,s_b = self.index_to_state[i]

            #print(str(s_a) + ', ' + str(s_b))
            outcome_a = self.is_over((s_a + 1, s_b), self.goal, self.lead, self.golden, self.best_of)
            outcome_b = self.is_over((s_a    , s_b + 1), self.goal, self.lead, self.golden, self.best_of)
            #print('Outcome: ' + str(outcome_a) + ' state: ' + str((s_a +1,s_b)))
            #print('Outcome: ' + str(outcome_b) + ' state: ' + str((s_a ,s_b +1)))

            self.calculate_next_index(outcome_a, (s_a+1, s_b), i, available_indexes, self.wp)
            self.calculate_next_index(outcome_b, (s_a, s_b+1), i, available_indexes, self.lp)

        return self.index_to_state, self.state_to_index

    def add_lead_indexes(self, valid_indexes):
        adv_states        = valid_indexes[self.goal**2:]
        valid_indexes     = valid_indexes[:self.goal**2]
        advantage = 1
        assert len(adv_states) % 2 == 0
        while len(adv_states) > 0 and advantage < self.lead:
            a_adv, b_adv = adv_states.pop(0), adv_states.pop(0)
           # This code may be unnecessary
           #a_win_index, a_lose_index = a_adv + 2, a_adv - 2
           #b_win_index, b_lose_index = b_adv - 2, b_adv + 2
           #if advantage == 1:
           #    a_lose_index = a_adv - 1
           #if advantage == self.lead - 1:
           #    a_win_index  = win_index
           #    b_lose_index = lose_index
            self.index_to_state[a_adv] = ('adv', advantage)
            self.state_to_index[('adv',advantage)]  = a_adv
            self.index_to_state[b_adv] = ('adv', -advantage)
            self.state_to_index[('adv',-advantage)] = b_adv
            advantage += 1
        return valid_indexes

    def calculate_next_index(self, outcome, state, cur_index, available_indexes, p):
        # No won on outcome. There will be complications here
        if outcome == 0:
          # Check if state has already been populated
            if state not in self.index_to_state.values():
              # Available index will be reduced in size
                next_index                             = available_indexes.pop(0) 
                self.index_to_state[next_index]        = state
                self.state_to_index[state]             = next_index
            else:
                next_index = self.state_to_index[state]
        elif outcome == 1 or outcome == 3:
            if outcome == 3: # Skeleton implementation for golden point stat
                pass
        elif outcome == -1 or outcome == -3:
            if outcome == -3:
                pass
        # Check if advantage state has been created for this specific advantage
        if outcome == 2 or outcome == -2:
            # Calculates advantage
            s_a, s_b        = state
            advantage       = s_a - s_b
            advantage_state = ('adv',advantage)
  
            # Check if we have already visited this state
            if advantage_state not in self.state_to_index:
                next_index = available_indexes.pop(0)
                self.index_to_state[next_index] = advantage_state
                self.state_to_index[advantage]  = next_index
            else:
                next_index = self.state_to_index[advantage_state]

    '''
        Positive values: winner a
        Negative values: winner b
        -3: winner b golden point
        -2: winner b within lead
        -1: winner b
        0 : no win
        1 : winner a
        2 : winner a within lead
       3 : winner a golden point
    '''
    @staticmethod
    def is_over(state, goal, lead, golden, best_of):
        s_a, s_b = state

        # First check: best of has been reached
        if best_of is not None:
            win_best_of_a = s_a >= math.ceil(best_of / 2)
            win_best_of_b = s_b >= math.ceil(best_of / 2)
            if win_best_of_a:
                return 1
            if win_best_of_b:
                return -1
            return 0 # Best of winning score has not been reached by any player

        # Second check: golden point has been reached
        reached_golden_a = s_a >= golden
        reached_golden_b = s_b >= golden
        if reached_golden_a:
            return 3
        if reached_golden_b:
            return -3

        # Third check: any of the players has won
        within_lead      = abs(s_a - s_b) < lead
        win_a   = s_a >= goal and not within_lead
        win_b   = s_b >= goal and not within_lead
        if win_a:
            return 1
        if win_b:
            return -1


        # Fourth check: we are inside a deuce
        if s_a >= goal and s_a >= s_b and within_lead:
            return 2 if golden == float('inf') else 0
        if s_b >= goal and s_b >= s_a and within_lead:
            return -2 if golden == float('inf') else 0

        # Fifth check: match continues without special condition
        return 0
