from  __future__ import division
import game_level as gl
import math

class Sport:

    def __init__(self):
        self.name        = 'NO_NAME_GIVEN'
        self.level_rules = []
    

    # TODO: add checks like goal > lead
    def add_hierarchy_level(goal, lead, golden, best_of):
        # checks
        assert goal >= 1
        assert lead < goal
        levels.append((goal, lead, golden, best_of))


    # Actual simulator
    def play_match(spw=[None, None]): # add player names

        transition_matrix = self.get_transition_matrix()
        statistics = self.play(transition_matrix)

    def get_transition_matrix(self):
        exists_transition_matrix = False
        if not exists_transition_matrix:
            return self.generate_transition_matrix()
        else:
            return self.load_transition_matrix()

    '''
        Load transition matrix from a file. This will happen if sport was already created
    '''
    def load_transition_matrix(self):
        pass

    # TODO: document this function
    def generate_transition_matrix(self):
        num_absorbing_states  = 2 # win/lose states
        isolated_state_levels = map(self.calculate_number_of_states, self.level_rules)
        total_level_states    = self.aggregated_level_size(1,isolated_state_levels)
        transition_matrix = np.zeros(total_states[0]**2, total_level_states[0]**2 + num_absorbing_states)
        win_index  = total_level_states[0]
        lose_index = total_level_states[0] + 1
        initial_i  = 0
        # (map) loop over all your GameLevels until the matrix is fully complete # Create checks for matrix here: each row only has 2 non zero values...etc
        self.propatage_transitions(transition_matrix, initial_i,isolated_state_levels, 
                                    total_level_states, win_index, lose_index,
                                    self.level_rules)
        

    def propatage_transitions(self, matrix, initial, iso_level, total_levels,
                              win_i, lose_i, rules):
        cur_iso, cur_total = iso_level[0], total_levels[0]
        goal, lead, golden, best_of = rules[0]
        valid_indexes = range(initial, initial + cur_total, cur_iso)
        g = game_level.GameLevel(goal, lead, golden, best_of)
        g.populate_transition_matrix(matrix, cur_iso, valid_states, win_i, lose_i)
        for i, (win, lose) in g.index_connections:
            # This is not bottom up
            next_win_i, next_lose_i, next_initial = win,lose,0
            self.propatage_transitions(matrix, next_initial, iso_level[1:],
                                        total_levels[1:], next_win_i, next_lose_i,
                                        rules[1:])

    '''
        Calculates number of states according to the 3 input parameters: Goal, Lead, Golden
    '''
    def calculate_number_of_states(self, goal, lead, golden, best_of):
        if best_of is not None:
            return math.ceil(best_of / 2)**2
        # There is no golden
        if golden == 0 or golden == float('inf'): 
            return goal**2 + max(0, 2*(lead - 1))

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

    def aggregated_level_size(self, acc, x):
        total_level_states = x[:]
        acc = 1
        for i in range(1,len(x)):
            total_level_states = x[i] * acc
            acc *= x[i]
        return total_level_states
