// test_moving_average.cpp - a noisy sensor on A0: 2.0 V, jumping to 3.0 V at t = 2 s, with 0.1 V of noise
#include <random>
#include "run.h"
#include "avr_int.h"
#include "../moving_average/moving_average.ino"

int main() {
  static std::mt19937 gen(97);                           // fixed seed: the same noise every run
  static std::normal_distribution<double> noise(0.0, 0.1);
  sim::ain[A0] = [](double t) { return (t < 2.0 ? 2.0 : 3.0) + noise(gen); };
  sim::run_ms(4000);
}
