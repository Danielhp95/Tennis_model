"""
    Make some documentation here
"""

class matchLogger(object):

    '''
    Params:
        best_of     -> Represents best of 5 or best of 3 match

        mean_a, mean_b -> mean win serve probability for each player
        var_a, var_b   -> variance around the mean

        game_f      -> function that determines prob of player winning a game
        tie_break_b -> function that determines prob of player winning a tie_break 
        set_f       -> function that determines prob of player winning a set 
        serv_probability_f -> function that determines prob of player winning a serve
                       Initial parameters are fixed. Custom parameters can be added
                       at the end and retrived in *custom_args
    '''
    def __init__(self, best_of=None, mean_a=None, mean_b=None,
                 var_a=0, var_b=0, tie_break_f=None, game_f=None,
                 set_f=None,serv_probability_f=None):
        # Match stats
        self.best_of = best_of

        # Player stats
        self.mean_a = mean_a
        self.mean_b = mean_b
        self.var_a  = var_a
        self.var_b  = var_b

        # Match function pointers
        self.set_function_pointers(game_f, tie_break_f, set_f, serv_probability_f)

        # Buffers
        self.sets_score  = []
        self.final_score = []

    def set_function_pointers(self, game_f, tie_break_f, 
                              set_f, serv_probability_f):
        if game_f != None:
            self.game_f_name              = game_f.__module__ + '.' + game_f.__name__
        if tie_break_f != None:
            self.tie_break_f_name         = tie_break_f.__module__ + '.' + tie_break_f.__name__
        if set_f != None:
            self.set_f_name               = set_f.__module__ + '.' + set_f.__name__
        if serv_probability_f != None:
            self.serv_probability_f_name = serv_probability_f.__module__ + '.' + serv_probability_f.__name__

    def logSet(self, winner, game_score):
        self.sets_score.append(game_score)

    #TODO figure out if we care about winners
    def logMatch(self, winner, match_score):
        self.winner      = winner
        self.final_score = match_score

    def __str__(self):
        return str(self.sets_score)
