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
