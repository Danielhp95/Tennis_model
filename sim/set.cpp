#include <iostream>
#include <cassert>
#include <cmath>
#include <cstdlib>
#include <map>
#include <string>

using namespace std;

#include "formula.hpp"
#include "match.hpp"
#include "set.hpp"
#include "game.hpp"

bool Set::play_set (double *spw) {
  reset_set();

  while (!set_over()) {    
    bool tiebreak = (!final_set || tiebreaker_final_set) && games_won[0] == 6 && games_won[1] == 6;
    if (tiebreak) {
        assert(!final_set || tiebreaker_final_set);
	match->set_tiebreaker();
    }
    Game *current = new Game (match, tiebreak, spw);
    current->play_game();
    //cout << "SPW for the game: " << *spw << endl;
    //cout << "Game won by player_a " << current->player_won(0) << endl;
    if (current->player_won(0)) {
      games_won[0]++;
#ifdef VERBOSE
      cout << player(0)->name() << " wins a game!" << endl;
#endif
    } else {
      assert(current->player_won(1));
      games_won[1]++;
#ifdef VERBOSE
      cout << player(1)->name() << " wins a game!" << endl;
#endif
    }
    delete current;
  }
#ifdef VERBOSE
  cout << "end of set, score " << games_won[0] << "-" << games_won[1] << endl;
#endif
  
  return player_won(0);
}
