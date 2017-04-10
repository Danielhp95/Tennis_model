// 

// cat matchid160114111.htm | striphtml | grep '\$[0-9]' | grep -v '(' | head -4 | sed 's/\$//' | more


#include <iostream>
#include <iomanip>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cctype>
#include <cstring>
#include <string>
#include <cassert>

#define EPS 2.254e-16

using namespace std;

double M3_inversion[1000], M5_inversion[1000];

bool read_table(const char *filename, double *table, int length) {
  FILE *fp = fopen(filename,"r");
  assert(fp);
  table[0] = 0;
  double actual_x = 0, y;
  for (int n=1; n<length; n++) {
    double expected_x = (double) n / length;
    assert(fscanf(fp, " %lf %lf ", &actual_x, &y) == 2);
    assert(fabs(expected_x - actual_x) < 1e-06);
    table[n] = y;
  }
  return true;
}

double lookup(double *table, double p) {
  int index = (int) (p*1000.0);
  assert (index >=0 && index < 1000);
  return table[index];
}

double A[28][6] = { 
  {  1,3,0,4,0,0},
  {  3,3,1,4,0,0},
  {  4,4,0,3,1,0},
  {  6,3,2,4,0,0},
  { 16,4,1,3,1,0},
  {  6,5,0,2,2,0},
  { 10,2,3,5,0,0},
  { 40,3,2,4,1,0},
  { 30,4,1,3,2,0},
  {  4,5,0,2,3,0},
  {  5,1,4,6,0,0},
  { 50,2,3,5,1,0},
  {100,3,2,4,2,0},
  { 50,4,1,3,3,0},
  {  5,5,0,2,4,0},
  {  1,1,5,6,0,0},
  { 30,2,4,5,1,0},
  {150,3,3,4,2,0},
  {200,4,2,3,3,0},
  { 75,5,1,2,4,0},
  {  6,6,0,1,5,0},
  {  1,0,6,6,0,1},
  { 36,1,5,5,1,1},
  {225,2,4,4,2,1},
  {400,3,3,3,3,1},
  {225,4,2,2,4,1},
  { 36,5,1,1,5,1},
  {  1,6,0,0,6,1}
};
  
double B[21][6] = {
  {  1,3,0,3,0,0},
  {  3,3,1,3,0,0},
  {  3,4,0,2,1,0},
  {  6,2,2,4,0,0},
  { 12,3,1,3,1,0},
  {  3,4,0,2,2,0},
  {  4,2,3,4,0,0},
  { 24,3,2,3,1,0},
  { 24,4,1,2,2,0},
  {  4,5,0,1,3,0},
  {  5,1,4,5,0,0},
  { 40,2,3,4,1,0},
  { 60,3,2,3,2,0},
  { 20,4,1,2,3,0},
  {  1,5,0,1,4,0},
  {  1,0,5,5,0,1},
  { 25,1,4,4,1,1},
  {100,2,3,3,2,1},
  {100,3,2,2,3,1},
  { 25,4,1,1,4,1},
  {  1,5,0,0,5,1}
};

double _TBpq(double p, double q) {
  //  cout << "in TB p = " << p << " q = " << q << endl;
  double result = 0;
  double dpq = p*q/(1.0-(p*(1.0-q)+(1.0-p)*q));
  for (int i=0; i<28; i++) {
    double contrib = A[i][0]*pow(p,A[i][1])*pow(1.0-p,A[i][2])*pow(q,A[i][3])*pow(1.0-q,A[i][4])*pow(dpq,A[i][5]);
    //    cout << "contrib[" << i << "] = " << contrib << endl;
    result += contrib;
  }
  return result;
}  

double TB(double p1, double p2) {
  return _TBpq(p1,1.0-p2);
}

double G(double p) {
  return pow(p,4)*(15.0 - 4.0*p - 10.0*p*p/(1.0-2.0*p*(1.0-p)));
}

double _Spq(double p, double q) {
  double gp=G(p);
  double gq=G(q);

  double result = 0.0;

  double contrib;

  for (int i=0; i<21; i++) {

    double contrib1 = log(B[i][0]) +
      B[i][1]*log(gp) +
      B[i][2]*log(1.0-gp)+
      B[i][3]*log(gq) +
      B[i][4]*log(1-gq) +
      B[i][5]*log(gp*gq+(gp*(1.0-gq)+(1.0-gp)*gq)*_TBpq(p,q));
		  		  
    double contrib2 = B[i][0]*pow(gp,B[i][1])*pow(1.0-gp,B[i][2])*pow(gq,B[i][3])*pow(1.0-gq,B[i][4])*pow(gp*gq+(gp*(1.0-gq)+(1.0-gp)*gq)*_TBpq(p,q),B[i][5]);
    
    //    cout << fabs(exp(contrib1) - contrib2) << endl;
    result += exp(contrib1);
  }

  return result;
}

double S(double p1, double p2) {
  return _Spq(p1, 1.0-p2);
}

double _M3pq(double p, double q) {
  double spq = _Spq(p,q);
  return spq*spq*(1.0+2.0*(1.0-spq));
}

double M3(double p1, double p2) {
  return _M3pq(p1, 1.0-p2);
}

double _M5pq(double p, double q) {
  double spq = _Spq(p,q);
  return spq*spq*spq*(1.0+3.0*(1.0-spq)+6.0*(1.0-spq)*(1.0-spq));
}

double M5(double p1, double p2) {
  return _M5pq(p1, 1.0-p2);
}

double M5_invert_p1(double implied_odds) {
  assert(implied_odds > 0);
  //  double implied_odds = 1.0/odds;
  
  double p2 = 0.60;
  double best_p2 = 0.6;
  double best_p1 = 0.05;
  double best_match = 1.0;
  
  for (double p1 = best_p1; p1<=0.95; p1+=0.0001) {
    double outcome = M5(p1,p2);
    if (fabs(outcome - implied_odds) < best_match) {
      best_p1 = p1;
      best_match = fabs(outcome - implied_odds);
    }
  }
   
  //  cout << "best_p1 = " << best_p1 << " (" << best_match << ")" << endl;
  return best_p1 - best_p2;
}

double M5_invert_p2(double implied_odds) {
  assert(implied_odds > 0);
  //  double implied_odds = 1.0/odds;
  
  double p1 = 0.60;
  double best_p1 = 0.6;
  double best_p2 = 0.05;
  double best_match = 1.0;
  
  for (double p2 = best_p2; p2<=0.95; p2+=0.0001) {
    double outcome = M5(p1,p2);
    if (fabs(outcome - implied_odds) < best_match) {
      best_p2 = p2;
      best_match = fabs(outcome - implied_odds);
    }
  }
   
  //  cout << "best_p2 = " << best_p2 << " (" << best_match << ")" << endl;
  return best_p1 - best_p2;
}

double M5_invert(double implied_odds) {
  return (M5_invert_p1(implied_odds)+M5_invert_p2(implied_odds))/2.0;
}


// return p1 - p2 most likely to give odds on player p1
double M3_invert_p1(double implied_odds) {
  assert(implied_odds > 0);
  //  double implied_odds = 1.0/odds;
  
  double p2 = 0.60;
  double best_p2 = 0.6;
  double best_p1 = 0.05;
  double best_match = 1.0;
  
  for (double p1 = best_p1; p1<=0.95; p1+=0.0001) {
    double outcome = M3(p1,p2);
    if (fabs(outcome - implied_odds) < best_match) {
      best_p1 = p1;
      best_match = fabs(outcome - implied_odds);
    }
  }
   
  //  cout << "best_p1 = " << best_p1 << " (" << best_match << ")" << endl;
  return best_p1 - best_p2;
}

double M3_invert_p2(double implied_odds) {
  assert(implied_odds > 0);
  //  double implied_odds = 1.0/odds;
  
  double p1 = 0.60;
  double best_p1 = 0.6;
  double best_p2 = 0.05;
  double best_match = 1.0;
  
  for (double p2 = best_p2; p2<=0.95; p2+=0.0001) {
    double outcome = M3(p1,p2);
    if (fabs(outcome - implied_odds) < best_match) {
      best_p2 = p2;
      best_match = fabs(outcome - implied_odds);
    }
  }
   
  //  cout << "best_p2 = " << best_p2 << " (" << best_match << ")" << endl;
  return best_p1 - best_p2;
}

double M3_invert(double implied_odds) {
  return (M3_invert_p1(implied_odds)+M3_invert_p2(implied_odds))/2.0;
}

bool file_exists(string filename) {
  FILE *fp = fopen(filename.c_str(), "r");
  if (fp) {
    fclose(fp);
    return true;
  }
  return false;
}

double extract_stat(const char *statistic, int first) {
  double result = 0;
  int afterlines = (first) ? 1 : 2, pn = 0, pd = 0;
  char buffer[1024];
  sprintf(buffer, "cat stats.html | grep \"%s\" -m 1 -A %d | tail -1 | sed 's/\\%%.*(/ /g' | sed 's/\\// /g' | sed 's/).*//g'", statistic, afterlines);
  FILE *fp = popen(buffer, "r");
  assert(fp);
  //  cout << buffer << endl;
  if (fscanf(fp, " %lf %d %d ",&result, &pn, &pd) < 3)
    return -1;

  //  cout << "result = " << result << " pn = " << pn << " pd = " << pd << endl;
  assert(pd >= 0);
  assert( fabs(double(pn)/pd*100.0 - result) < 5);
  pclose(fp);
  return double(pn)/pd*100.0;
}

int extract_match_statistics(string target, string opponent, char *stats_file, double &tspw, double &trpw) {

  assert(file_exists(stats_file));

  char buffer[1024];
  sprintf(buffer, "cat %s | striphtml | sed 's/\t//g' | grep '[0-9A-Za-z].*' > stats.html", stats_file);
  system(buffer);
  sprintf(buffer, "cat stats.html | grep -A 1 \"%s\" | grep \"%s\" | wc -l", target.c_str(), opponent.c_str());
  //  cout << buffer << endl;
  FILE *fp = popen(buffer, "r");
  int first = 0;
  fscanf(fp," %d" ,&first);
  assert(first == 0 || first==1);
  pclose(fp);
  if (first == 0) {
    sprintf(buffer, "cat stats.html | grep -A 1 \"%s\" | grep \"%s\" | wc -l", opponent.c_str(), target.c_str());
  //  cout << buffer << endl;
    fp = popen(buffer, "r");
    int second = 0;
    fscanf(fp," %d" ,&second);
    assert(second==1);
    pclose(fp);
  }
  cerr << "#" << target << " is " << (first ? "first" : "second" )<< " in stats." << endl;

  /*  fsp = extract_stat("1st Serve",first);
  assert(fsp > 0 && fsp <= 100);
  fspwp = extract_stat("1st Serve Points Won",first);
  assert(fspwp > 0 && fspwp <= 100);
  sspwp = extract_stat("2nd Serve Points Won",first);
  assert(sspwp > 0 && sspwp <= 100);
  fsrwp = extract_stat("1st Return Points Won",first);
  if (fsrwp <= 0)
  fsrwp = extract_stat("1st Serve Return Points Won",first);*/
  //assert(fsrwp > 0 && fsrwp <= 100);
  /*
  ssrpwp = extract_stat("2nd Return Points Won",first);
  if (ssrpwp <= 0)
  ssrpwp = extract_stat("2nd Serve Return Points Won",first);*/
  //assert(ssrpwp > 0 && ssrpwp <= 100);
  tspw = extract_stat("Total Service Points Won",first);
  assert(tspw > 0 && tspw <= 100);
  trpw = extract_stat("Total Return Points Won",first);
  assert(trpw > 0 && trpw <= 100);
  return 1;
}

bool get_minimum_buy_in(char *match_file, double &one, double &two) {

  int line_two = 0;

  one = two = 1000.0;

  char buffer[1024], input[1024];

  sprintf(buffer,"grep -c '^not available$' %s",match_file);
  FILE *fp = popen(buffer, "r");
  assert(fp);
  fgets(input, 1024, fp);
  pclose(fp);
//  cout << "buffer = " << buffer << endl;
//  cout << "input = " << input << endl;
  int count = 0;
  if (sscanf(input," %d ", &count) != 1)
    return false;

  if (count > 0) {
    assert(count == 2);
    line_two = 3;
  } else 
    line_two = 4;

  sprintf(buffer,"./striphtml < %s | grep '\\$[0-9]' | grep -v '(' | head -1 | sed 's/\\$//'",match_file);
  
  fp = popen(buffer, "r");
  assert(fp);
  fgets(input, 1024, fp);
  pclose(fp);

  if (sscanf(input," %lf ", &one) != 1)
    return false;

  sprintf(buffer,"./striphtml < %s | grep '\\$[0-9]' | grep -v '(' | head -%d | tail -1 | sed 's/\\$//'",match_file,line_two);

  fp = popen(buffer, "r");
  assert(fp);
  fgets(input, 1024, fp);
  pclose(fp);

  if (sscanf(input," %lf ", &two) != 1)
    return false;

  cerr << "minimum buy ins: " << one << ", " << two << endl;
  
  return true;
}

string get_scoreline(char *match_file) {

  char buffer[1024], input[1024];

  sprintf(buffer,"./striphtml < %s | grep -A8 DEFEATED | tail -1",match_file);
  
  FILE *fp = popen(buffer, "r");
  assert(fp);
  fgets(input, 1024, fp);
  pclose(fp);

  for (int n=0; n<strlen(input); n++) {
    if (isspace(input[n]) && input[n] != ' ')
      input[n] = '\0';
  }
  
  string result(input);

  return result;
}

char *read_dash(char *str) {
  while (*str && *str != '-')
    str++;
  if (*str == '-')
    str++;
  return str;
}

char *ignore_braces(char *str) {
  if (str && *str == '(') {
    while (*str != '\0'  && *str != ')')
      str++;
  }
  return str;
}

char *read_number(char *str, int &number) {
  number = 0;
  while (*str && !isdigit(*str))
    str++;
  if (isdigit(*str)) {
    sscanf(str, " %d ", &number);
    while (isdigit(*str))
      str++;
    return str;
  } else
    return NULL;
}

bool process_scoreline(string scoreline) {
  char str[1024];
  strcpy(str, scoreline.c_str());
  //  cout << "SCORELINE: " << str << endl;
  char *input = &str[0];

  int set[2], one = 0, two = 0;
  set[0] = set[1] = 0;

  while (input) {
    one = two = 0;
    //    cout << "input: " << input << endl;
    input = read_number(input, one);
    if (!input) break;
    //    cout << "one: " << one << endl;
    //    cout << "input: " << input << endl;
    input = read_dash(input);
    //    cout << "input: " << input << endl;
    input = read_number(input, two);
    assert(input);
    //    cout << "two: " << two << endl;
    input = ignore_braces(input);
    //    cout << "SET SCORE: " << one << "-" << two << " " << endl;
    if (one > two)
      set[0]++;
    else 
      set[1]++;
  }
  //  assert(set[0] + set[1] == 3 || set[0] + set[1] == 5);
  
  return (set[0] == 0 || set[1] == 0);
}

bool clean_string(char *target, char delimiter) {
  for (int n=0; n<strlen(target); n++)
    if (target[n] == delimiter) {
      target[n] = '\0';
      return true;
    }
  return false;
}

int get_tips(char *target) {
  int result = 0;
  char *colon = strchr(target, ':');
  assert(colon);
  if (sscanf(colon + 1, " %d ", &result) == 1)
    return result;
  return 0;
}

bool get_market_preds(char *match_file, string &p1, string &p2, double implied_market_odds[2]) {

  double min_one, min_two;
  get_minimum_buy_in(match_file, min_one, min_two);

  char buffer[1024], input[1024], name1[1024], name2[1024];
  double odds1, odds2;

  sprintf(buffer,"./striphtml < %s | grep -A3 'Moneyline'| head -3 ",match_file);
  
  implied_market_odds[0] = implied_market_odds[1] = 0;

  FILE *fp = popen(buffer, "r");
  assert(fp);
  fgets(input, 1024, fp);
  fgets(name1, 1024, fp);
  fgets(name2, 1024, fp);
  pclose(fp);

  int tips1 = get_tips(name1);
  int tips2 = get_tips(name2);
  cerr << "# tips1 = " << tips1 << " tips2 = " << tips2 << endl;

  clean_string(name1,':');
  clean_string(name2,':');

  p1 = name1;
  p2 = name2;

  sscanf(input, "Moneyline Summary (%lf/%lf)", &odds1, &odds2);
  cerr << "# Moneyline Summary (" << odds1 << "/" << odds2 << ")" << endl;

  char odds1str[100], odds2str[100];
  if (odds1 > 0 && odds2 > 0) {
    implied_market_odds[0] = 1.0/odds1;
    implied_market_odds[1] = 1.0/odds2;
    double sum = implied_market_odds[0] + implied_market_odds[1];
    implied_market_odds[0]/=sum;
    implied_market_odds[1]/=sum;
//    if (tips1/implied_market_odds[0] > tips2/implied_market_odds[1])
      cout << odds1*100.0-100 << " -100 " << odds1 << " " << odds2 << " " << (double) tips1/(tips1+tips2)/implied_market_odds[0] << " " << double (tips2)/(tips1+tips2)/implied_market_odds[1] << " " << min_one << " " << min_two << " " << match_file << " \"" << p1 << "\" \"" << p2 << "\"" << endl;
//    else if (tips1/implied_market_odds[0] < tips2/implied_market_odds[1])
//      cout << -100 << " " << odds2 << " " << tips1/implied_market_odds[0] << " " << tips2/implied_market_odds[1] << " " << min_one << " " << min_two << " " << match_file << " \"" << p1 << "\" \"" << p2 << "\"" << endl;
    return true;
  } 	   
  return false;
}

bool analyse_match(char *stats_file, char *match_file) {

  string p1, p2;
  double implied_market_odds[2];

  if (!file_exists(stats_file) || !file_exists(match_file))
    return false;

  get_market_preds(match_file, p1, p2, implied_market_odds);
/*
  if (get_market_preds(match_file, p1, p2, implied_market_odds)) {

    cerr << "# " << p1 << " v " << p2 << endl;
    cerr << "# implied market odds = " << implied_market_odds[0] << "/" << implied_market_odds[1] << endl;

    double implied_diff = lookup(M3_inversion, implied_market_odds[0]);

    cerr << "# implied_diff = " << implied_diff << endl;

    string scoreline = get_scoreline(match_file);
    bool straight_sets = process_scoreline(scoreline);
    cerr << "# scoreline is " << scoreline << " straight_sets = " << straight_sets << endl;

    double tspw = 0, trpw = 0;
    extract_match_statistics(p1, p2, stats_file, tspw, trpw);
    
    double actual_p1 = tspw, actual_p2 = 100.0 - trpw;
    
    cerr << "# actual_p1 = " << actual_p1 << " actual_p2 = " << actual_p2 << endl;
    double actual_diff = actual_p1 - actual_p2;

    cerr << "# actual diff = " << actual_diff << endl;

    string report("SS");
    if (!straight_sets)
      report = "PS";

    if (implied_market_odds[0] >= 0.5)
      cout << implied_diff << " " << actual_diff << " \"" << p1 << " d. " << p2 << "\" " << report << " 1" << endl;
    else
      cout << implied_diff << " " << -actual_diff << " \"" << p1 << " d. " << p2 << "\" " << report << " -1" << endl;
   

  }
*/
  return true;
}

double sign(double x) {
  if (x<-EPS)
    return -1;
  if (x>EPS)
    return 1;
  return 0;
}

double root_of_quintic(double a, double b, double c, double d, double e, double f) {

  double left = 0;
  double right = 1.0;
  double mid = 0.5, f_mid = 0.0;

  do {

    mid = (left + right)/2.0;
    //    cout << "(" << left << ", " << right << ") " << mid << endl;
    
    double f_left = a*left*left*left*left*left+b*left*left*left*left+c*left*left*left+d*left*left+e*left+f;
    if (sign(f_left) == 0)
      return left;
    double f_right = a*right*right*right*right*right+b*right*right*right*right+c*right*right*right+d*right*right+e*right+f;
    if (sign(f_right) == 0)
      return right;
    f_mid = a*mid*mid*mid*mid*mid+b*mid*mid*mid*mid+c*mid*mid*mid+d*mid*mid+e*mid+f;
    
    //    cout << "f_left = " << f_left << endl;
    //    cout << "f_right = " << f_right << endl;
    //    cout << "f_mid = " << f_mid << endl;

    assert( sign(f_left) != sign(f_right));

    if (sign(f_left) == sign (f_mid)) {
      left = mid;
    } else if (sign(f_right) == sign(f_mid)){
      right = mid;
    }

  } while (sign(f_mid) != 0 && fabs(left - right) > 1e-08);

  return mid;
}

double root_of_cubic(double a, double b, double c, double d) {

  double left = 0;
  double right = 1.0;
  double mid = 0.5, f_mid = 0.0;

  do {

    mid = (left + right)/2.0;
    //    cout << "(" << left << ", " << right << ") " << mid << endl;
    
    double f_left = a*left*left*left+b*left*left+c*left+d;
    if (sign(f_left) == 0)
      return left;
    double f_right = a*right*right*right+b*right*right+c*right+d;
    if (sign(f_right) == 0)
      return right;
    f_mid = a*mid*mid*mid+b*mid*mid+c*mid+d;
    
    //    cout << "f_left = " << f_left << endl;
    //    cout << "f_right = " << f_right << endl;
    //    cout << "f_mid = " << f_mid << endl;

    assert( sign(f_left) != sign(f_right));

    if (sign(f_left) == sign (f_mid)) {
      left = mid;
    } else if (sign(f_right) == sign(f_mid)){
      right = mid;
    }

  } while (sign(f_mid) != 0 && fabs(left - right) > 1e-12);

  return mid;
}

double probability_of_winning_set_given_M3(double p) {
  //  return root_of_cubic(2,-3,0,p);
  return root_of_quintic(0,0,2,-3,0,p);
}  

double probability_of_winning_set_given_M5(double p) {
  return root_of_quintic(6,-15,10,0,0,-p);
}  

  /*
  double delta = 18.0*a*b*c*d - 4.0*b*b*b*d + b*b*c*c - 4.0*a*c*c*c - 27.0*a*a*d*d;

  cout << "delta = " << delta << endl;
  
  double delta0 = b*b - 3.0*a*c;
  double delta1 = 2.0*b*b*b - 9.0*a*b*c + 27.0*a*a*d;

  double delta2 = delta1*delta1 - 4*delta0*delta0*delta0;
  cout << "delta2 = " << delta2 << endl;
  cout << "delta2 = " << -27.0*a*a*delta << endl;
  assert(delta2 > 0);

  double C = exp(1.0/3.0*log( (delta1 + sqrt(delta2))/2.0 ));

  double x1 = -1.0/(3.0*a)*(b + C + delta0/C);

  cout << "x1 = " << x1 << endl;*/
//  return x1;
//}

int main(int argc, char *argv[]) {

  //cout << M3_invert(0.72) << endl; 
  cout << M3(0.72,0.65) << endl;
  //cout << M3(0.815,0.805) << endl;

  return 0;  
/* 
  double root1 = probability_of_winning_set_given_M3(0.78300180831826401446);
  double root2 = probability_of_winning_set_given_M3(1-0.78300180831826401446);
  cout << root1 << endl;
  cout << root2 << endl;

  return 0;
*/
  for (double p=0; p<=1.0; p+=0.1) {
    double root = probability_of_winning_set_given_M5(p);
    double opp_root = probability_of_winning_set_given_M5(1-p);

    cout << "for " << p << " root = " << root << " opp_root = " << opp_root << " " << root+opp_root << endl;
  }

  return 0;

  read_table("M3invert.dat", M3_inversion, 1000);
  //  read_table("M5invert.dat", M5_inversion, 1000);

  /*  for (double p=0.001; p<1.0; p+=0.001)
    cout << p << " " << M5_invert(p)*100.0 << endl;

    return 0;*/

  assert(argc >= 2);

  // argv[1] should be the stats file of the match we are supposed to analyse.
  // argv[2] should be the match file of the match we are supposed to analyse.

  analyse_match(argv[1],argv[2]);

  /*
  cout << "=================================== A =================================" << endl;

  for (int i=0; i<28; i++) {
    for (int j=0; j<6; j++) {
      cout << setw(10) << A[i][j] << " ";
    }
    cout << endl;
  }

  cout << "=================================== B =================================" << endl;

  for (int i=0; i<21; i++) {
    for (int j=0; j<6; j++) {
      cout << setw(10) << B[i][j] << " ";
    }
    cout << endl;
  }

  cout << pow(2,0) << endl;
  */  
  /*  double p1 = 0.6, p2 = 0.55;

  cout << "p1 = " << p1 << endl;
  cout << "p2 = " << p2 << endl;

  cout << "G(p1) = " << G(p1) << endl;
  cout << "G(p2) = " << G(p2) << endl;
  cout << "TB(p1,p2) = " << TB(p1,p2) << " (TB(p2,p1)=" << TB(p2,p1) << ")" << endl;
  cout << "S(p1,p2) = " << S(p1,p2) << " (S(p2,p1)=" << S(p2,p1) << ")" << endl;
  cout << "M3(p1,p2) = " << M3(p1,p2) << " (M3(p2,p1)=" << M3(p2,p1) << ")" << endl;
  cout << "M5(p1,p2) = " << M5(p1,p2) << " (M5(p2,p1)=" << M5(p2,p1) << ")" << endl;
  */
  /*  cout << "M3(0.6, 0.6338) = " << M3(0.6, 0.6338)  << endl;
  cout << "M3(0.5662, 0.6) = " << M3(0.5662, 0.6)  << endl;
  cout << "M3_invert(0.3333333) = " << M3_invert_p1(1.0/3.0) << endl;
  cout << "M3_invert_p1(0.3333333) = " << M3_invert_p1(1.0/3.0) << endl;
  cout << "M3_invert_p2(0.3333333) = " << M3_invert_p2(1.0/3.0) << endl;*/

  return 0;
}
