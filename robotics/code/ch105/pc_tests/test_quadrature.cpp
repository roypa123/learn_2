// test_quadrature.cpp - the wheel turns forwards at 1,305 pulses/s for 2 s, then backwards at 650 pulses/s for 1 s.
// Channel B is a quarter of a pulse behind A when going forwards (ahead of it when going backwards).
#include <cmath>
#include "run.h"
#include "avr_int.h"
#include "../quadrature/quadrature.ino"

double phase(double t) { return t < 2.0 ? 1305.0 * t : 2610.0 - 650.0 * (t - 2.0); }
int square(double p) { return (p - std::floor(p)) < 0.5 ? LOW : HIGH; }

int main() {
  sim::din[2] = [](double t) { return square(phase(t)); };          // channel A
  sim::din[4] = [](double t) { return square(phase(t) - 0.25); };   // channel B
  sim::run_ms(3050);
}
