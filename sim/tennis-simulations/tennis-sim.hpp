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

#include "formula.hpp"
#include "match.hpp"
#include "set.hpp"
#include "game.hpp"

using namespace std;

double spw(int player_index, int *total_serves, int *total_serves_won);
double win_match_probability(int player_index, int *winner, int total_matches);
double win_set_probability(int player_index, int *winner, int total_matches);
double average_game_length(int total_games, int num_matches);
double median_game_length(std::vector<int> game_lengths, int num_matches);
std::vector<double> confidence_interval(std::vector<double> v, int confidence);
