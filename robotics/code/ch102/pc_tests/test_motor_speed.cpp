// test_motor_speed.cpp - the knob on A0 is turned in steps: 0, 0.8, 2.0, 3.5 and 5.0 V
#include "run.h"
#include "avr_int.h"
#include "../motor_speed/motor_speed.ino"

int main() {
  sim::ain[A0] = [](double t) { return t < 0.2 ? 0.0 : t < 0.4 ? 0.8 : t < 0.6 ? 2.0 : t < 0.8 ? 3.5 : 5.0; };
  sim::run_ms(1000);
}
