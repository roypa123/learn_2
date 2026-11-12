// test_read_volts.cpp - the voltage on A0 steps through 0, 1.0, 2.5, 3.1 and 4.99 V, half a second each
#include "run.h"
#include "avr_int.h"
#include "../read_volts/read_volts.ino"

int main() {
  sim::ain[A0] = [](double t) { return t < 0.5 ? 0.0 : t < 1.0 ? 1.0 : t < 1.5 ? 2.5 : t < 2.0 ? 3.1 : 4.99; };
  sim::run_ms(2400);
}
