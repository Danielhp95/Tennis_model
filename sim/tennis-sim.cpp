//cat activity10307.html | sed 's/<td /\n<td /g' | striphtml | grep -v "^&nbsp;" | grep -v '^\$' | awk 'BEGIN { odds = 0; } { if (odds) print $0;} /^Odds/ { odds = 1;  }' | grep -v '^>' | sed 's/Recap//' | sed 's/Match Stats//'

// take into account most recent matches played as follows:

// if A is going to beat B then:
// A should be able to beat some players B has lost to (at least
// more players than B should beat that A has lost to) 
// B should lose to some players A has won against
// recursive approach with convincing H2H as terminating case?

// idea:

// make a reliability metric, based on how well for *each* common opponent, 
// the one player appears better than the other

// incorporate omalley formula

// idea:

// build up a first service % profile in terms of mean and std dev
// from previous matches, then use 90th percentiles in best and worst
// performances

// idea:

// use fsp not from matches but from short term player stats. hence normalise performance against common opponents to remove variations in fsp?

//cat activity.out | sed 's/<td /\n<td /g' | grep 'Lost to' | sed 's/.*.htm\">//' | sed 's/<a href.*//' | sed 's/<\/a>([0-9,.]*)//' | sed 's/([A-Z]*).*//g' | sort | uniq


// to do:
//   add medium duration
//   add player stats to save
//   automatically get current odds from match pages
//   automatically get results from match pages

#include <iostream>
#include <fstream>
#include <cassert>
#include <cstring>
#include <cctype>
#include <ctime>
#include <cmath>
#include <cstdlib>
#include <map>
#include <vector>
#include <algorithm>
#include <string>

#define TRIALS 50

using namespace std;

#include "formula.hpp"
#include "match.hpp"
#include "set.hpp"
#include "game.hpp"

int main(int argc, char *argv[]) {

  if (argc < 7) {
    cout << "usage: " << argv[0] << " 2/3 adv/tie <spw1> <stddev1> <spw2> <stddev2> [<game target>]" << endl; 
    return 0;
  }
  bool five_sets = true;

  if (strchr(argv[1],'2')) {
    five_sets = false;
    cout << "playing best of 3 sets" << endl;
  } else {
    five_sets = true;
    cout << "playing best of 5 sets" << endl;
  } 
  
  bool tiebreaker_final_set = true; //false;
  if (tolower(argv[2][0]) == 'a') {
    tiebreaker_final_set = false;
    cout << "advantage final set" << endl;
  } else {
    cout << "tiebreak final set" << endl;
  }

  double spw1 = atof(argv[3]);
  double stddev1 = atof(argv[4]);
  double spw2 = atof(argv[5]);
  double stddev2 = atof(argv[6]);

  cout << "spw1 = " << spw1 << " stddev1 = " << stddev1 << endl;
  cout << "spw2 = " << spw2 << " stddev2 = " << stddev2 << endl;

  double target_games = 0;
  if (argc >= 8) {
    target_games = atof(argv[7]);
    cout << "examining games target of " << target_games << endl;
  }

  int set_limit = (five_sets ? 3 : 2);

  srand48(time(NULL));
  int winner[2], outcomes[4][4], wins_set[2], wins_straight_sets[2];
  int tiebreak_matches = 0;
 
  winner[0] = winner[1] = 0;
  wins_set[0] = wins_set[1] = 0;
  wins_straight_sets[0] = wins_straight_sets[1] = 0;
 
  for (int i=0; i<=3; i++)
	for (int j=0; j<=3; j++)
	  	outcomes[i][j] = 0;

  long matches_over = 0, matches_under = 0;
  double total_games = 0;

  std::vector<int> game_lengths;
  for (int n=0; n<TRIALS; n++) {
    if (n % 1000 == 0){
        cout << "Games so far: " << n << endl;
    }
    Match m(spw1, stddev1, spw2, stddev2, five_sets, tiebreaker_final_set);
    m.play_match();
    total_games += m.total_games();
    game_lengths.push_back(m.total_games()); 
    if (m.total_games() > target_games)
     matches_over++;
    if (m.total_games() < target_games)
     matches_under++;
    if (m.player_won(0))
	winner[0]++;   
    else {
        assert(m.player_won(1));
        winner[1]++;
    }
    int sets_p1 = m.sets_won(0);
    int sets_p2 = m.sets_won(1);
    if (m.tiebreaker())
      tiebreak_matches++;
   
    if (sets_p1 > 0)
      wins_set[0]++;
    if (sets_p2 > 0)
      wins_set[1]++;

    if (sets_p1 == 0)
      wins_straight_sets[1]++;
    if (sets_p2 == 0)
      wins_straight_sets[0]++;
 
    assert(sets_p1 >= 0 && sets_p1 <= (five_sets ? 3 : 2) );
    assert(sets_p2 >= 0 && sets_p2 <= (five_sets ? 3 : 2) );
    outcomes[sets_p1][sets_p2]++;
  }

  sort(game_lengths.begin(), game_lengths.end());
  cout << TRIALS << " matches simulated."  << endl << endl;
  
  for (int p=0; p<2; p++) 
    cout << "Player " << p + 1 << " wins match with probability " << (double) winner[p]/TRIALS << " (fair odds " << (double) TRIALS/winner[p] << ")" << endl;
  cout << endl;

  for (int p=0; p<2; p++) 
    cout << "Player " << p + 1 << " wins a set with probability " << (double) wins_set[p]/TRIALS << " (fair odds " << (double) TRIALS/wins_set[p] << ")" << endl;
  cout << endl;

  for (int p=0; p<2; p++) 
    cout << "Player " << p + 1 << " wins in straight sets with probability " << (double) wins_straight_sets[p]/TRIALS << " (fair odds " << (double) TRIALS/wins_straight_sets[p] << ")" << endl;
  cout << endl;
  cout << "Probability of tiebreaker: " << (double) tiebreak_matches/TRIALS << " (fair odds " << (double) TRIALS/tiebreak_matches << ")" << endl;
  cout << endl;
  cout << "Median match length in games is " << (double) (game_lengths[TRIALS/2-1]+game_lengths[TRIALS/2])/2.0 << endl;
  cout << "Average match length in games is " << (double) total_games/TRIALS << endl;
  if (target_games > 0) {
    cout << "Probability of match under " << target_games << " games is " << (double) matches_under/TRIALS << " (fair odds " << (double) TRIALS/matches_under << ")" << endl;
    cout << "Probability of match over " << target_games << " games is " << (double) matches_over/TRIALS << " (fair odds " << (double) TRIALS/matches_over << ")" << endl;
  }
  return 0;
}
