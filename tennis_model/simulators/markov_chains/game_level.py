from __future__ import division
import numpy as np
import math

class GameLevel:



    def __init__(self, goal=None, lead=1, golden=float("inf"), best_of=None, number_of_serves=None):
        self.wp      = 9999  # will need to turn this into variables
        self.lp      = -9999 # These are not used here
        self.number_of_serves = number_of_serves
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


    """
        Coolest function in the whole class
        Calculates the states for this game level given a set of valid indexes. Search through the state space
        is conducted in a breadth-first traversal manner.
    """
    def calculate_states_from_indexes(self, number_of_transient_states, valid_indexes):
        # Initialize state population
        initial_index = valid_indexes[0]
        initial_state = (0,0)
        self.index_to_state[initial_index] = (0,0)
        self.state_to_index[initial_state] = initial_index

        if self.golden == float('inf') and self.lead > 0:
            valid_indexes = self.add_lead_indexes(valid_indexes)

        available_indexes = valid_indexes[1:]
        for i in valid_indexes:
            s_a ,s_b = self.index_to_state[i]

            outcome_a = self.is_over((s_a + 1, s_b), self.goal, self.lead, self.golden, self.best_of)
            outcome_b = self.is_over((s_a    , s_b + 1), self.goal, self.lead, self.golden, self.best_of)

            self.calculate_next_index(outcome_a, (s_a+1, s_b), i, available_indexes, self.wp)
            self.calculate_next_index(outcome_b, (s_a, s_b+1), i, available_indexes, self.lp)

        return self.index_to_state, self.state_to_index

    # Test this
    def add_lead_indexes(self, valid_indexes):
        #May need to change this. to reduce the 
        if self.number_of_serves is None:
            adv_states        = valid_indexes[self.goal**2:]
            valid_indexes     = valid_indexes[:self.goal**2]
        else:
            adv_states        = valid_indexes[(self.goal**2-1):]
            valid_indexes     = valid_indexes[:(self.goal**2-1)]

        # The reason why we have this separation is to differentiate
        # the cases where the server does not change
        # and server changing midway through the game level.
        if self.number_of_serves is None:
            for advantage in range(1,self.lead):
                a_adv, b_adv = adv_states.pop(0), adv_states.pop(0)
                self.index_to_state[a_adv] = ('adv', (advantage,'',0))
                self.state_to_index[('adv',(advantage,'',0))]  = a_adv
                self.index_to_state[b_adv] = ('adv', (-advantage,'',0))
                self.state_to_index[('adv',(-advantage,'',0))] = b_adv
        else: # Case where the server changes in this game level.
            flatten = lambda x,y: x + y # Flattens a list
            # advantages go in pairs, [1,-1,2,-2...lead-1,-lead+1)]
            for advantage in [0] + reduce(flatten,[[adv,-adv] for adv in range(1,self.lead)]):
                # Assume advantage for 0 is already there
                for server in ['a','b']: # Am I doing less breadth-first and more sweeping?
                    for consecutive_serves in range(0, self.number_of_serves):
                        state = ('adv', (advantage, server, consecutive_serves))
                        adv_index = adv_states.pop(0)
                        self.index_to_state[adv_index] = state
                        self.state_to_index[state]     = adv_index
        return valid_indexes

    def calculate_next_index(self, outcome, state, cur_index, available_indexes, p):
        # Case where the state (goal -1, goal-1) becomes a deuce state
        if self.number_of_serves is not None and self.lead > 1 and state == (self.goal-1, self.goal-1):
            # This is already covered in add lead indexes, this is advantage zero state
            return
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
            players = ['a','b']
            k       = s_a + s_b # What point we are in the game level
            if self.number_of_serves is None:
                server = ''
                consecutive_serves = 0
            else:
                server_index  = math.floor(k/self.number_of_serves) % len(players)
                server  = players[server_index]
                consecutive_serves = k % self.number_of_serves
            advantage_state = ('adv',(advantage,server,consecutive_serves))

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
    def is_over(state, goal, lead, golden, best_of,number_of_serves=None):
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
        # Deuce condition concept changes if the server changes in this game level.
        normal_deuce_condition = lambda s_a, s_b: (s_a >= goal or s_b >= goal)
        number_of_states_deuce_condition = lambda s_a, s_b: (s_a >= goal or s_b >= goal) or (s_a == goal -1 and s_b == goal -1)
        deuce_condition = lambda s_a,s_b: normal_deuce_condition(s_a,s_b) if (number_of_serves is None and lead > 1) else number_of_states_deuce_condition(s_a,s_b)
        if deuce_condition(s_a,s_b) and s_a >= s_b and within_lead:
            return 2 if golden == float('inf') else 0
        if deuce_condition(s_a,s_b) and s_b >= s_a and within_lead:
            return -2 if golden == float('inf') else 0

        # Fifth check: match continues without special condition
        return 0

