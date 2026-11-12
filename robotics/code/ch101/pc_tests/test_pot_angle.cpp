// test_pot_angle.cpp - the potentiometer on A1 is turned in five steps from one end to the other
#include "run.h"
#include "avr_int.h"
#include "../pot_angle/pot_angle.ino"

int main() {
  sim::ain[A1] = [](double t) { return t < 0.5 ? 0.0 : t < 1.0 ? 1.25 : t < 1.5 ? 2.5 : t < 2.0 ? 3.75 : 5.0; };
  sim::run_ms(2400);
}
