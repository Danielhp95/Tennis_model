class Game {
private:
  Match *match;
  const double *_spw;
  int points_played;
  int points_won[2];
  bool tiebreak; 
  bool result; /* true = player1 wins, false = player 2 wins */

  void reset_game() {
    points_played = 0;
    points_won[0] = 0;
    points_won[1] = 0;
  }
public:

  Game(Match *_match, bool _tiebreak, const double *spw) {
    match = _match;
    tiebreak = _tiebreak;
    _spw = spw;
    reset_game();
  }

  #define QUICK

  bool play_game() {
  
    match->increase_games();
    int target = 4;

#ifdef QUICK
   //http://www.amstat.org/chapters/boston/nessis07/presentation_material/James_OMalley.pdf
   //http://www.stat.columbia.edu/~vecer/tennis.pdf 
   //http://robert-farrenkopf.info/tennis/tennis1.htm
   if (!tiebreak) {
      int server = !match->player1_serving();
  //    cout << "QUICK server = " << server << " ";
      int receiver = !server;
      //double in_p = (player(server)->first_serve_in_percent()+match->noise(server))/100.0;
      //     double p = in_p*player(server)->first_service_points_won_percent_against_player(*player(receiver))/100.0 + (1.0-in_p)*player(server)->second_service_points_won_percent_against_player(*player(receiver))/100.0;
      double p = _spw[server]; //player(server)->service_points_won_percent_against_player(*player(receiver))/100.0;
      double game_p =  pow(p,4)*(15.0 - 4.0*p - 10.0*p*p/(1.0-2.0*p*(1.0-p)));
      //double game_p2 =  pow(p,4)*(15.0 - 34.0*p + 28.0* p*p - 8.0*p*p*p)/(1.0-2.0*p+2*p*p);
      //cout << "QUICK p = " << p << " game_p = " << game_p << " game_p2 = " << game_p2 << endl;
      double randperc = drand48();       
      double server_wins = (randperc < game_p) ? true : false;
      result = (match->player1_serving()) ? server_wins : !server_wins;
      match->switch_server();
      return result;
   } 
#endif

    if (tiebreak) {
#ifdef VERBOSE
      cout << "playing a tiebreak" << endl;
#endif
      target = 6;
    }

    bool player1_serving_start = match->player1_serving();


    while (!game_over(target)) {

      int server = !match->player1_serving();
      int receiver = !server;
#ifdef VERBOSE
      cout << "server is " << server << " receiver is " << receiver << endl;
#endif
      double randperc = drand48()*100.0;

      result = (randperc < _spw[server]) ? true : false;

      if (result) {
	points_won[server]++;
      } else {
	points_won[receiver]++;    	
      }

#ifdef VERBOSE
      cout << "server = "<< points_won[server] << " receiver = " << points_won[receiver] << endl;
#endif
      
      points_played++;

      if (tiebreak && points_played % 2 == 1) {
	match->switch_server();
      }

    }
    
    if (match->player1_serving() == player1_serving_start)
      match->switch_server();
   
    result = player_won(0, target); 
#ifdef VERBOSE
    cout << "game won by ";
    if (player_won(0, target))
      cout << player(0)->name() << " (" << points_won[0] << "-" << points_won[1] << ")" << endl;
    else
      cout << player(1)->name() << " (" << points_won[1] << "-" << points_won[0] << ")" << endl;
#endif

    return player_won(0, target);
  }

  bool player_won(int player) {
    return (player == 0) ? result : !result;
  }
/*
  Player *player(int _player) {
    return (match->player(_player));
  }
*/
  bool player_won(int player, int target) {
    return (points_won[player] >= target && points_won[!player] < (points_won[player] - 1));
  }

  bool game_over(int points) {
    return player_won(0, points) || player_won(1, points);
  }

};
