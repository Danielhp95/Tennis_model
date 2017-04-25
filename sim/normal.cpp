#include <iostream>
#include <cstdlib>

using namespace std;

class Normal {
private:
  double mu, stddev;
public:
  Normal() {
    mu = 0;
    stddev = 1;
  }
  Normal(double _mu, double _stddev) {
    mu = _mu;
    stddev = _stddev;
  }
  double next() {
    double sum = 0;
    for (int n=0; n<12; n++)
      sum += drand48();
    sum -= 6;
    return sum*stddev + mu;
  }
};
/*
int main() {
  Normal Z;

  int bin[121];

  for (int n=0; n<121; n++)
    bin[n] = 0;

  for (int n=0; n<100000; n++) {
    double z = Z.next();
    int bin_number = ((z+6)*10);
    bin[bin_number]++;
  }  

  for (int n=0; n<121; n++)
    cout << (n/10.0-6.0) << " " << bin[n]/100000.0 << endl;
  return 0;
} */
