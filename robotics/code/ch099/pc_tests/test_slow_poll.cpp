// test_slow_poll.cpp - eight quick, clean presses of 60 ms each
#include "run.h"
#include "avr_int.h"
#include "../slow_poll/slow_poll.ino"

int main() {
  static const double downs[8] = {250, 830, 1410, 2120, 2700, 3390, 4050, 4610};
  sim::din[2] = [](double t) {
    double ms = t * 1000;
    for (double d : downs) {
      if (ms >= d && ms < d + 60) return LOW;
    }
    return HIGH;
  };
  sim::run_ms(5000);
}
