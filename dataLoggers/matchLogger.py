"""
    Make some documentation here
"""

class matchLogger(object):

    # serv_distribution can be fixed, gaussian
    # Match type: M3, M5
    # League: ATP, WTP
    def __init__(self, serv_dist, match_type, league):
        self.serv_dist  = serv_dist
        self.match_type = match_type
        self.league     = league

    def logGame(self, winner, score):
        return 

    def logSet(self, winner, score):
        return

    def logMatch(self, winner, score):
        return 
