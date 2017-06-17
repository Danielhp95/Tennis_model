from  __future__ import division
import markov_chain_utils as mcu
import game_level as gl
import numpy as np
import math

class Sport:

    def __init__(self):
        self.name        = 'NO_NAME_GIVEN'
        self.level_rules = []
    
    def add_hierarchy_level(self, goal=0, lead=0, golden=float('inf'), best_of=None):
        # checks
        if best_of is None:
            assert goal >= 1
            assert lead <= goal
        self.level_rules.append((goal, lead, golden, best_of))

    def compute_transition_matrix(self):
        # State space size for each level of the hirarchy
        isolated_level_states = self.isolated_level_size()
        # State space that each unit of a level of the hierarchy requires
        total_level_states    = self.aggregated_level_size(isolated_level_states)
        self.total_states = total_level_states[0]

        # The actual transition matrix that defines the markov chain
        transition_matrix = self.initialize_transition_matrix(self.total_states) 
        # Last most two indexes will be used as columns for the absorbing states
        absorbing_win_index  = self.total_states
        absorbing_lose_index = self.total_states + 1

        # These indexes will be used to determine where each game level is placed in final transition matrix
        all_valid_indexes = self.generate_all_valid_indexes(isolated_level_states, total_level_states)

        # Absolute states. Each absolute state is represented as an array of tuples, where each tuple is the
        # score for a game level in the hierarchy.
        abs_in_to_st = self.calculate_all_absolute_states(all_valid_indexes, isolated_level_states, total_level_states)
        abs_st_to_in = {tuple(v) : k for k, v in abs_in_to_st.iteritems()} # Reverses dictionary

        # Add both absorbing states to dictionary containing 
        # a mapping between absolute states and their corresponding indexes
        abs_st_to_in[('win',)]  = absorbing_win_index
        abs_st_to_in[('lose',)] = absorbing_lose_index

        # Calculate where each state will lead to upon winning or losing a point
        index_conections = {index : (self.calculate_next_win_state(st),self.calculate_next_lose_state(st)) for index, st in abs_in_to_st.items()}
        # Transform value states into indexes 
        index_conections = {index : (abs_st_to_in[tuple(win_s)], abs_st_to_in[tuple(los_s)]) for index, (win_s, los_s) in index_conections.items()}

        # Having calculated which entries in the matrix will need to be populated with some transition probability.
        # The final step is to decide the value of all transition probabilities.
        # This is done by using serve propagation rules.

        transition_matrix = self.propagate_serve_rules(transition_matrix, 
                                                       abs_st_to_in, abs_in_to_st,
                                                       index_conections,
                                                       isolated_level_states, 
                                                       total_level_states)

        return transition_matrix

    # TODO: Complete function
    def compute_winning_probabilities(self, spw=[None, None]):
        transition_matrix = self.compute_transition_matrix() # May need to pass spw tp function
        Q = transition_matrix[:,:self.total_states]
        I = np.eye(self.total_states)
        R = transition_matrix[:,self.total_states:]
        player_win_probabilities = mcu.calculate_absorption_probabilities(Q,I,R)
        return player_win_probabilities
        

    def initialize_transition_matrix(self, num_transient_states):
        # First two variables are in desceding order.
        num_absorbing_states  = 2 # Win and Lose absorbing states
        transition_matrix = np.zeros((num_transient_states, num_transient_states + num_absorbing_states))
        return transition_matrix

    # Generates all valid indexes that will be used to calculate where each game state will be located
    # This is done by calculating where each level of the hierarchy will begin. This is possible because
    # we know the size of every game level in the whole match.
    def generate_all_valid_indexes(self, isolated_level_sizes, total_level_sizes):
        all_valid_indexes = [] # lxi matrix. Where l = number of game levels; i = instances of game level. Kinda...
        total_match_size  = total_level_sizes[0]

        # TODO: see if this can be done in two list comprehensions
        for i in range(0, len(total_level_sizes)):
            current_level_instances_valid_indexes = []
            lower_level_instance_size = total_level_sizes[i+1] if i+1 < len(total_level_sizes) else 1
            current_level_total_size  = total_level_sizes[i]
            for initial in range(0,total_match_size, current_level_total_size):
                current_level_instances_valid_indexes.append(range(initial, initial + current_level_total_size, lower_level_instance_size))

            all_valid_indexes.append(current_level_instances_valid_indexes)

        return all_valid_indexes

    def calculate_all_absolute_states(self, val_i, iso_level_sizes, total_level_sizes):
        abs_in_to_st = {}
        for i in range(0, len(val_i)):
            for j in range(0, len(val_i[i])):
                g = gl.GameLevel(*self.level_rules[i])
                in_to_st, _ = g.calculate_states_from_indexes(iso_level_sizes[i], val_i[i][j])
                in_to_st    = {k : self.absolute_state_from_relative(v, i, j, val_i, abs_in_to_st) for k, v in in_to_st.items()}
                abs_in_to_st.update(in_to_st)
        return abs_in_to_st

    # Given an initial absolute state, it will return the state that will come if player a wins the point
    def calculate_next_win_state(self, state):
        next_win_state = state[:]
        for i in range(len(state)-1,-1,-1):
            s_a, s_b = state[i]
            level_goal, level_lead, _, _ = self.level_rules[i]
            # We are inside a deuce
            if s_a == 'adv':
                if s_b < level_lead - 1:
                    new_advantage = s_b + 1
                    next_win_state[i] = ('adv',new_advantage) if new_advantage !=0 else (level_goal -1, level_goal-1)
                    return next_win_state
                else:
                    next_win_state[i] = (0,0)
                    continue

            outcome  = gl.GameLevel.is_over((s_a + 1, s_b),*self.level_rules[i])
            if outcome == 0:
                # We don't move from current game level
                next_win_state[i] = (s_a+1,s_b)
                return next_win_state 
            if outcome == 2: # No need to worry about Best_of because lead and best_of are mutually exclusive
                advantage = (s_a + 1) - s_b
                next_win_state[i] = ('adv', advantage) if advantage != 0 else (level_goal -1, level_goal-1)
                return next_win_state
            if outcome == 1 or outcome == 3:
                # We move to next game level. We reset this level
                next_win_state[i] = (0,0)
                continue
        return [('win')]

    # Given an initial absolute state, it will return the state that will come if player a loses the point
    def calculate_next_lose_state(self, state):
        next_lose_state = state[:]
        for i in range(len(state)-1,-1,-1):
            s_a, s_b = state[i]
            level_goal, level_lead, _, _ = self.level_rules[i]
            # We are inside a deuce
            if s_a == 'adv':
                if s_b > -1*(level_lead - 1):
                    new_advantage = s_b - 1
                    next_lose_state[i] = ('adv',new_advantage) if new_advantage !=0 else (level_goal -1, level_goal-1)
                    return next_lose_state
                else:
                    next_lose_state[i] = (0,0)
                    continue

            outcome  = gl.GameLevel.is_over((s_a, s_b+1),*self.level_rules[i])
            if outcome == 0:
                # We don't move from current game level
                next_lose_state[i] = (s_a,s_b+1)
                return next_lose_state 
            if outcome == -2: # No need to worry about Best_of because lead and best_of are mutually exclusive
                advantage = s_a - (s_b + 1)
                next_lose_state[i] = ('adv', advantage) if advantage != 0 else (level_goal -1, level_goal-1)
                return next_lose_state
            if outcome == -1 or outcome == -3:
                # We move to next game level. We reset this level
                next_lose_state[i] = (0,0)
                continue
        return [('lose')]

    # TODO: document
    # Figure out sweetly tomorrow afternoon.
    def absolute_state_from_relative(self, rel_st, cur_level, cur_index, valid_indexes, abs_states):
        flatten = lambda x,y: x + y 
        if cur_level - 1 < 0:
            higher_states = []
        else:
            flattened_list = reduce(flatten, valid_indexes[cur_level - 1])
            state_above_index = flattened_list[cur_index]
            higher_states     = abs_states[state_above_index][:cur_level]
        lower_states  = [(0,0)] * (len(valid_indexes) - (cur_level + 1))
        current_absolute_state = higher_states + [rel_st] + lower_states
        return current_absolute_state

    # Winning is seen as player A winning
    def propagate_serve_rules(self, transition_matrix, abs_st_to_in, abs_in_to_st, index_conections, isolated_level_states, total_level_states):
        for i in range(0, len(transition_matrix)):
            win_i = index_conections[i][0] if index_conections[i][0] != 'win' else absorbing_win_index
            los_i = index_conections[i][1] if index_conections[i][1] != 'lose' else absorbing_lose_index
            # Change may need to happen to accomodate adv winn states.
            transition_matrix[i,win_i] = 1
            transition_matrix[i,los_i] = -1
        return transition_matrix

    def aggregated_level_size(self, x):
        return [reduce(lambda x,y: x*y, x[i:]) for i in range(0,len(x))] # What an obscure and beautiful line of code

    def isolated_level_size(self):
        return map(lambda (goal, lead, golden, best_of): self.calculate_number_of_states(goal, lead, golden, best_of), self.level_rules)

    '''
        Calculates number of states according to the 4 input parameters: Goal, Lead, Golden, Best_of
    '''
    def calculate_number_of_states(self, goal, lead, golden, best_of, number_of_serves=None):
        if best_of is not None:
            return int(math.ceil(best_of / 2)**2)
        # There is no golden
        if golden == 0 or golden == float('inf'): 
            if number_of_serves is None or lead <= 1:
                return goal**2 + max(0, 2*(lead - 1))
            else:
                number_advantage_state_clusters = 1 + (lead-1)*2
                size_advantage_state_clusters   = 2*number_of_serves # constant 2 refers to number of players
                return goal**2 -1 + number_advantage_state_clusters*size_advantage_state_clusters

        
        # Golden case
        total_states = 0
        max_range = 2*golden
        for i in range(0, max_range + 1): # State-space is being computed unnecesarily. Wanna optimize it ;) ?
            a_score      = range(i,-1,-1)
            b_score      = range(0,i+1)
            pos_states   = zip(a_score, b_score)
            valid_states = filter(lambda st: self.is_valid_state(st, goal, lead, golden, best_of),
                                  pos_states)
            total_states += len(valid_states)
        return total_states

    def is_valid_state(self, state, goal, lead, golden, best_of):
        outcome = gl.GameLevel.is_over(state, goal, lead, golden, best_of)
        return outcome == 0 or outcome == 2 or outcome == -2
