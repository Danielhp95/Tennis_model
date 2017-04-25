//#define NOISE

class Player;
class Set;

class Match {
private:
  //Player *_player[2];
  double _spw[2];
  bool _player1_serving;
  int _sets_to_win, sets_played, _sets_won[2];
  double _noise[2];
  Set *set[5];
  bool _tiebreaker;
  bool _tiebreaker_final_set;
  int _total_games;
  int _serves[2]
  int _serves_won[2];

  void reset_match() {
    sets_played = 0;
    _total_games = 0;
    _sets_won[0] = 0;
    _sets_won[1] = 0;
    _serves[0] = 0;
    _serves[1] = 0;
    _serves_won[0] = 0;
    _serves_won[1] = 0;
    _player1_serving = (drand48() > 0.5);
    _tiebreaker = false;
  }

public:
  Match(double spw1, double stddev1, double spw2, double stddev2, bool five_sets, bool tiebreaker_final_set);

  bool match_over() {
    return player_won(0) || player_won(1);
  }

  bool player_won(int __player) { return _sets_won[__player] >= _sets_to_win; }
  
  void print_score() {
  }

  void increase_games() {
    _total_games++;
  }

  bool play_match();

  bool player1_serving() {
    return _player1_serving;
  }

  bool switch_server() {
    _player1_serving = !_player1_serving;
    return _player1_serving;
  }

/*  Player *player(int __player) {
    return _player[__player];
  }

  double noise(int __player) {
    return _noise[__player];
  }*/

  int sets_to_win() const { return _sets_to_win; }

  int sets_won(int player) { return _sets_won[player]; }

  
  void increase_serves(int player) { return _serves_won
  int serves_won(int player) { return _serves_won[player]; }

  bool tiebreaker() const { return _tiebreaker; }

  void set_tiebreaker() { _tiebreaker = true; }

  int total_games() { return _total_games; }
};
