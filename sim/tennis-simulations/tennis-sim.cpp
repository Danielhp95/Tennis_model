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

#include "tennis-sim.hpp"

using namespace std;

#define TRIALS 100

//Debugging purposes
void print_vector(std::vector<double> v) {
  for (auto i : v) {
      cout << i << ' ';
  }
  cout << endl;
}

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

  //Better document these.
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

  // Variables used to calculate spw 
  int total_serves[2]     = {0,0};
  int total_serves_won[2] = {0,0};
  std::vector<double> a_matches_spw;
  std::vector<double> b_matches_spw;

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

    total_serves[0] += m.serves_played(0);
    total_serves[1] += m.serves_played(1);
    total_serves_won[0] += m.serves_won(0);
    total_serves_won[1] += m.serves_won(1);
    a_matches_spw.push_back((double)m.serves_won(0)/m.serves_played(0));
    b_matches_spw.push_back((double)m.serves_won(1)/m.serves_played(1));
  }
  cout << TRIALS << " matches simulated."  << endl << endl;

  // Sorting simulated data
  sort(game_lengths.begin(), game_lengths.end());
  sort(a_matches_spw.begin(), a_matches_spw.end());
  sort(b_matches_spw.begin(), b_matches_spw.end());

  std::vector<double> sliced_a_matches = confidence_interval(a_matches_spw, 95);
  cout << sliced_a_matches.size() << endl;

  return 0;
  for (int p=0; p<2; p++) {
    cout << "Player " << p + 1 << " served this many times: " << (double) total_serves[p] << endl;
    cout << "Player " << p + 1 << " serve win probability: " << spw(p, total_serves, total_serves_won) << endl;
  }  
  cout << endl;
  for (int p=0; p<2; p++) 
    cout << "Player " << p + 1 << " wins match with probability " << win_match_probability(p, winner, TRIALS)<< " (fair odds " << (double) TRIALS/winner[p] << ")" << endl;
  cout << endl;

  for (int p=0; p<2; p++) 
    cout << "Player " << p + 1 << " wins a set with probability " << win_set_probability(p, wins_set, TRIALS) << " (fair odds " << (double) TRIALS/wins_set[p] << ")" << endl;
  cout << endl;

  for (int p=0; p<2; p++) 
    cout << "Player " << p + 1 << " wins in straight sets with probability " << win_set_probability(p, wins_straight_sets, TRIALS) << " (fair odds " << (double) TRIALS/wins_straight_sets[p] << ")" << endl;
  cout << endl;
  cout << "Probability of tiebreaker: " << (double) tiebreak_matches/TRIALS << " (fair odds " << (double) TRIALS/tiebreak_matches << ")" << endl;
  cout << endl;
  cout << "Median match length in games is " << median_game_length(game_lengths, TRIALS)  << endl;
  cout << "Average match length in games is " << average_game_length(total_games, TRIALS) << endl;
  if (target_games > 0) {
    cout << "Probability of match under " << target_games << " games is " << (double) matches_under/TRIALS << " (fair odds " << (double) TRIALS/matches_under << ")" << endl;
    cout << "Probability of match over " << target_games << " games is " << (double) matches_over/TRIALS << " (fair odds " << (double) TRIALS/matches_over << ")" << endl;
  }
  return 0;
}

double spw(int player_index, int *total_serves, int *total_serves_won) {
    return (double) total_serves_won[player_index]/total_serves[player_index];
}

double win_match_probability(int player_index, int *winner, int total_matches) {
    return (double) winner[player_index]/total_matches;
}

double win_set_probability(int player_index, int *wins_set, int total_matches){
    return (double) wins_set[player_index]/total_matches;
}

double average_game_length(int total_games, int num_matches) {
    return (double) total_games/num_matches;
}

double median_game_length(std::vector<int> game_lengths, int num_matches) {
    if (num_matches % 2 == 0) {
        return (double) (game_lengths[num_matches/2] +
                         game_lengths[(num_matches/2) - 1])/2;
    } else { return game_lengths[num_matches / 2]; }
}

// Vector MUST be sorted before calling this function
// Slices the vector to create a confidence interval
std::vector<double> confidence_interval(std::vector<double> v, int confidence) {
    assert(std::is_sorted(v.begin(), v.end()));
    int length = v.size();
    cout << length << endl;
    int first = ((double)length/100)*((double)(100-confidence)/2);
    cout << first << endl;
    int last  = length*(confidence + ((double)(100-confidence)/2))/100;
    cout << last << endl;

    std::vector<double>::const_iterator first_it = v.begin() + first;
    std::vector<double>::const_iterator last_it  = v.begin() + last;

    return std::vector<double>(first_it, last_it);
}

