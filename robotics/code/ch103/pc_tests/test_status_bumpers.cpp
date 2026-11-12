// test_status_bumpers.cpp - two clean bumps, at 1234.567 ms and 2345.678 ms, while the red light flashes
#include "run.h"
#include "avr_int.h"
#include "../status_bumpers/status_bumpers.ino"

int main() {
  sim::din[4] = [](double t) {
    double ms = t * 1000;
    return ((ms >= 1234.567 && ms < 1434.567) || (ms >= 2345.678 && ms < 2545.678)) ? LOW : HIGH;
  };
  sim::run_ms(3000);
}
