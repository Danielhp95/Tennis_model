#include <iostream>
#include <cassert>
#include <cmath>
#include <map>
#include <string>
#include <cstdlib>
#include <cstring>

using namespace std;

#include "formula.hpp"
#include "match.hpp"
#include "normal.hpp"
#include "set.hpp"

Match::Match(double spw1, double stddev1, double spw2, double stddev2, bool five_sets, bool tiebreaker_final_set) {

  _spw[0] = spw1;
  _spw[1] = spw2; 

  Normal z1(0,stddev1), z2(0, stddev2);
  _noise[0] = z1.next();
  _noise[1] = z2.next();

//cout << "noise[0] = " << _noise[0] << endl;
//cout << "noise[1] = " << _noise[1] << endl;

  _sets_to_win = (five_sets) ? 3 : 2;
  _tiebreaker_final_set = tiebreaker_final_set;
  reset_match();
}


bool Match::play_match() {
  reset_match();
  double noisy_spw[2];
  for (int x=0; x<2; x++) {
    noisy_spw[x] = _spw[x] + _noise[x];
    if (noisy_spw[x] < 0)
      noisy_spw[x] = 0;
    if (noisy_spw[x] > 100)
      noisy_spw[x] = 100;
  //  noisy_spw[x] /= 100.0; TODO: think this through
  //  Input probabilities are already between 0-1.
  //  It makes no sense to divide by 100 then.
  }
  while (!match_over()) {
   
    bool final_set = (_sets_won[0] == _sets_to_win - 1) && (_sets_won[1] == _sets_to_win - 1);	
    set[sets_played] = new Set(this, final_set, _tiebreaker_final_set);
    set[sets_played]->play_set(noisy_spw);
    if (set[sets_played]->player_won(0)) {
      _sets_won[0]++;
#ifdef VERBOSE
      cout << player(0)->name() << " wins a set!" << endl;
#endif
    } else {
      assert(set[sets_played]->player_won(1));
      _sets_won[1]++;
#ifdef VERBOSE
      cout << player(1)->name() << " wins a set!" << endl;
#endif
    }
    sets_played++;
  }

#ifdef VERBOSE
  if (player_won(0))
    cout << player(0)->name() << " wins (" << _sets_won[0] << " sets to " << _sets_won[1] << ")" << endl;
  else
    cout << player(1)->name() << " wins (" << _sets_won[1] << " sets to " << _sets_won[0] << ")" << endl;
#endif
  return player_won(0);
}
