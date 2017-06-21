from  __future__ import division
import markov_chain_utils as mcu
import game_level as gl
import numpy as np
import math

class Sport:


    def __init__(self, name='Unnamed sport', serve_win_probabilities=[1,-1]):
        self.name                    = name
        self.serve_win_probabilities = serve_win_probabilities
        self.level_rules             = []
        self.NUM_OF_PLAYERS = 2
    
    def add_hierarchy_level(self, goal=0, lead=0, golden=float('inf'), best_of=None, number_of_serves=None):
        # checks
        if best_of is None:
            assert goal >= 1
            assert lead <= goal
        self.level_rules.append((goal, lead, golden, best_of, number_of_serves))

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
        print(abs_in_to_st)
        index_conections = {index : (self.calculate_next_win_state(st),self.calculate_next_lose_state(st)) for index, st in abs_in_to_st.items()}
        #print(index_conections)
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

    # Returns the probabilities of
    # all transient states being absorbed by each absorbing state
    def compute_winning_probabilities(self, spw=[None, None]):
        transition_matrix = self.compute_transition_matrix() # May need to pass spw tp function
        Q = transition_matrix[:,:self.total_states]
        I = np.eye(self.total_states)
        R = transition_matrix[:,self.total_states:]
        player_win_probabilities = mcu.calculate_absorption_probabilities(Q,I,R)
        return player_win_probabilities
        
    # Initializes the transition probability matrix
    # by creating a matrix of the right dimensions and filling it with zeros.
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

    # In these function each game level maps their given indexes to relative states.
    # Each relative state is converted into absolute state.
    def calculate_all_absolute_states(self, val_i, iso_level_sizes, total_level_sizes):
        abs_in_to_st = {}
        for i in range(0, len(val_i)):
            for j in range(0, len(val_i[i])):
                g = gl.GameLevel(*self.level_rules[i])
                in_to_st, _ = g.calculate_states_from_indexes(iso_level_sizes[i], val_i[i][j])
                in_to_st    = {k : self.absolute_state_from_relative(v, i, j, val_i, abs_in_to_st) for k, v in in_to_st.items()}
                # Add all values from dictionary 'in_to_st' to dictionary 'abs_in_to_st'
                abs_in_to_st.update(in_to_st)
        return abs_in_to_st

    # Given an initial absolute state, it will return the state that will come if player a wins the point
    def calculate_next_win_state(self, state):
        next_win_state = state[:]
        for i in range(len(state)-1,-1,-1):
            s_a, s_b = state[i]
            level_goal, level_lead, level_golden, level_best_of, level_number_of_serves= self.level_rules[i]
            # We are inside a deuce
            if s_a == 'adv':
                advantage,server,consecutive_serves = s_b
                if advantage < level_lead - 1: # Check if minimum lead has been reached
                    new_advantage = advantage + 1
                    if level_number_of_serves is None:
                        new_server             = ''
                        new_consecutive_serves = 0
                        relative_next_win_state = ('adv',(new_advantage,new_server,new_consecutive_serves)) if new_advantage !=0 else (level_goal -1, level_goal-1)
                    else:
                        relative_next_win_state = self.next_advantage_state_multiple_serves(new_advantage,
                                                          server,
                                                          consecutive_serves,
                                                          level_number_of_serves)
                    next_win_state[i] = relative_next_win_state
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
                if level_number_of_serves is None:
                    relative_next_win_state = ('adv', (advantage,'',0)) if advantage != 0 else (level_goal -1, level_goal-1)
                else:
                    relative_next_win_state = self.next_advantage_state_multiple_serves(advantage, 
                                                      None,
                                                      None, level_number_of_serves,
                                                      s_a=s_a,s_b=s_b)
                next_win_state[i] = relative_next_win_state
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
            # Technical debt: create dictionary of level_rules. Unpacking not cool
            level_goal, level_lead, level_golden, level_best_of, level_number_of_serves= self.level_rules[i]
            # We are inside a deuce
            if s_a == 'adv':
                advantage,server,consecutive_serves = s_b
                if advantage > -1*(level_lead - 1):
                    new_advantage = advantage - 1
                    if level_number_of_serves is None:
                        new_server             = ''
                        new_consecutive_serves = 0
                        relative_next_lose_state = ('adv',(new_advantage,new_server,new_consecutive_serves)) if new_advantage !=0 else (level_goal -1, level_goal-1)
                    else:
                        relative_next_lose_state = self.next_advantage_state_multiple_serves(new_advantage,
                                                          server,
                                                          consecutive_serves,
                                                          level_number_of_serves)

                    next_lose_state[i] = relative_next_lose_state
                    return next_lose_state
                else:
                    next_lose_state[i] = (0,0)
                    continue

            outcome  = gl.GameLevel.is_over((s_a, s_b+1),*self.level_rules[i])
            if outcome == 0:
                # We don't move from current game level
                next_lose_state[i] = (s_a,s_b+1)
                return next_lose_state 
            # Technical debt having outcome == 2 here instead of -2
            if outcome == -2 or outcome == 2: # No need to worry about Best_of because lead and best_of are mutually exclusive
                advantage = s_a - (s_b + 1)
                if level_number_of_serves is None:
                    relative_next_lose_state = ('adv', (advantage,'',0)) if advantage != 0 else (level_goal -1, level_goal-1)
                else:
                    relative_next_lose_state = self.next_advantage_state_multiple_serves(advantage, 
                                                      None,
                                                      None, level_number_of_serves,
                                                      s_a=s_a,s_b=s_b)
                next_lose_state[i] = relative_next_lose_state
                return next_lose_state
            if outcome == -1 or outcome == -3:
                # We move to next game level. We reset this level
                next_lose_state[i] = (0,0)
                continue
        return [('lose')]

    # Calculates the next state knowing that number of serves is set and we are entering
    # a deuce state
    def next_advantage_state_multiple_serves(self, new_advantage, server,
                                             consecutive_serves, number_of_serves, 
                                             s_a=None,s_b=None):
        players = ['a','b']
        # These 2 conditionals are needed in case that input state
        # is not an advantage state itself
        if server is None and consecutive_serves is None:
            k = s_a + s_b
            server_index  = int(math.floor(k/number_of_serves)) % len(players)
            server  = players[server_index]
            consecutive_serves = k % number_of_serves
        
        new_consecutive_serves  = (consecutive_serves + 1) % number_of_serves
        change_server_condition = consecutive_serves + 1 >= number_of_serves
        new_server  = ('b' if server == 'a' else 'a') if change_server_condition else server
        new_consecutive_serves = (consecutive_serves + 1) % number_of_serves
        return ('adv',(new_advantage,new_server,new_consecutive_serves))


    '''
        rel_st: relative state that is to be expanded
        cur_level: Current hierarchical level for which we are calculating the abs state
        cur_index: Index in the list of valid indexes for the current level.
                   (NOT the valid index used to represent the state)
        valid_indexes: List of distributed valid indexes for all levels
        abs_states: Dictionary of already calculated absolute states

        Adds new absolute state from given relative state.
    '''
    def absolute_state_from_relative(self, rel_st, cur_level, cur_index, valid_indexes, abs_states):
        flatten = lambda x,y: x + y 
        if cur_level - 1 < 0:
            # We are at the top level, so there are no higher states
            higher_states = []
        else:
            # List of valid indexes for the level above the current level
            flattened_list = reduce(flatten, valid_indexes[cur_level - 1])
            state_above_index = flattened_list[cur_index]
            # State values for hierarchy levels above cur_level
            higher_states     = abs_states[state_above_index][:cur_level]
        # State values for hierarchy levels below cur_level, which are all (0,0)
        lower_states  = [(0,0)] * (len(valid_indexes) - (cur_level + 1))
        cur_absolute_state = higher_states + [rel_st] + lower_states
        return cur_absolute_state

    # Winning is seen as player A winning
    def propagate_serve_rules(self, transition_matrix, abs_st_to_in, abs_in_to_st, index_conections, isolated_level_states, total_level_states):
        spw_a, spw_b = self.serve_win_probabilities
        initial_server = 'a'
        cur_server = initial_server
        for i in range(0, len(transition_matrix)):
            win_i = index_conections[i][0] if index_conections[i][0] != 'win' else absorbing_win_index
            los_i = index_conections[i][1] if index_conections[i][1] != 'lose' else absorbing_lose_index
            win_p, los_p = self.calculate_win_and_lose_point_probabilities(i, cur_server, isolated_level_states, abs_in_to_st)
            # Change may need to happen to accomodate adv winn states.
            transition_matrix[i,win_i] = win_p
            transition_matrix[i,los_i] = los_p
        return transition_matrix


    def calculate_win_and_lose_point_probabilities(self, cur_index, cur_server, isolated_level_states, abs_in_to_st):
        spw_a, spw_b = self.serve_win_probabilities
        cur_absolute_state = abs_in_to_st[cur_index]
        levels_with_server_change = self.filter_game_levels_with_serving_rules()
        # Filter absolute state so that we only get the relative states for every game level
        # that has a change of serve
        initial_server = 0
        filtered_absolute_state = [(cur_absolute_state[i],level_rules) for (i,level_rules) in levels_with_server_change]
        server = reduce(self.calculate_server_for_level, filtered_absolute_state, initial_server)
        win_p, los_p = (spw_a,1-spw_a) if server == 0 else (1-spw_b,spw_b)
        return win_p, los_p

    def calculate_server_for_level(self,cur_server, level):
        state, rules =  level
        if state[0] == 'adv':
            server = 0 if state[1][1] == 'a' else 1 # Technical debt, change adv servers to numbers instead of letters
        else:
            s_a, s_b = state
            number_of_serves = rules[4]
            k = s_a + s_b
            server = math.floor(k/number_of_serves) % self.NUM_OF_PLAYERS
        return cur_server + server % self.NUM_OF_PLAYERS

    # TODO: May need to introduce here the rule of 'change server at the end of every game'
   # def calculate_win_and_lose_point_probabilities(self, cur_index, cur_server, isolated_level_states, abs_in_to_st):
   #     cur_absolute_state = abs_in_to_st[cur_index]
   #     levels_with_server_change = self.filter_game_levels_with_serving_rules()
   #     # Filter absolute state so that we only get the relative states for every game level
   #     # that has a change of serve
   #     filtered_absolute_state = [(cur_absolute_state[i],level_rules) for (i,level_rules) in levels_with_server_change]
   #     advantage_relative_states = [(rel_state, rules) for (rel_state, rules) in filtered_absolute_state if rel_state[0][0] == 'adv']
   #     normal_relative_states    = [(rel_state, rules) for (rel_state, rules) in filtered_absolute_state if rel_state[0][0] != 'adv']

   #     #advantage_states_change_of_server = [ c_s+1 == rules[3] for ((a,(adv,s,c_s),rules) in advantage_relative_states]
   #     advantage_states_change_of_server = [False]

   #     K = [s_a + s_b for ((s_a, s_b),rules) in normal_relative_states] # calculates K values for each game level.
   #     normal_states_change_of_server    = []
   #      
   #     # Check if any level of the hierarchy needs to change server
   #     server_needs_to_change = any(zip(advantage_states_change_of_server, normal_states_change_of_server))
   #     server = cur_server

   #     spw_a, spw_b = self.serve_win_probabilities
   #     win_p, los_p = spw_a, spw_b
   #     if server_needs_to_change:
   #         server = 'b' if server == 'a' else 'a'
   #     if server == 'a':
   #         win_p = spw_a
   #         los_p = 1 - spw_a
   #     else:
   #         win_p = 1 - spw_b
   #         los_p = spw_b
   #     server, win_p, los_p = cur_server, spw_a, spw_b
   #     return server, win_p, los_p

    # Calculates the aggreagated or total level size for all future game levels.
    def aggregated_level_size(self, x):
        return [reduce(lambda x,y: x*y, x[i:]) for i in range(0,len(x))] # What an obscure and beautiful line of code

    # Calculates the isolated level size for all future game levels.
    def isolated_level_size(self):
        return map(lambda rules: self.calculate_number_of_states(*rules), self.level_rules)
    
    # Filters all the game levels in order to get only those that are affected
    # by changing rules that change the server, their corresponding hierarchy level
    # is also returned.
    def filter_game_levels_with_serving_rules(self):
        # rules[4] is number of serves. Should really make it a dictionary
        return filter(lambda (i, rules): rules[4] is not None,
                      [(index, rules) for (index,rules) in enumerate(self.level_rules)])

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
