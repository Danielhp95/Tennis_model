class Set {

private:
  Match *match;
  int games_played;
  int games_won[2];
  bool final_set;
  bool tiebreaker_final_set;
  
  void reset_set() {
    games_played = 0;
    games_won[0] = 0;
    games_won[1] = 0;
  }

public:
  Set(Match *_match, bool _final_set, bool _tiebreaker_final_set) {
    match = _match;
    final_set = _final_set;
    tiebreaker_final_set = _tiebreaker_final_set;
  }

  bool player_won(int player) {
    if (!final_set || tiebreaker_final_set) 
      return (games_won[player] >= 6 && games_won[!player] < 5) || ((games_won[player] == 7 && games_won[!player] <= 6));
    return (games_won[player] >= 6 && games_won[!player] < games_won[player] - 1);
  }

  bool set_over() {
    return player_won(0) || player_won(1);
  }

/*  Player *player(int _player) {
    return match->player(_player);
  }*/

  bool play_set(double *spw);
};
