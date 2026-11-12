// test_bumpers.cpp - left bump at 1.0 s, right bump at 2.0 s, both at 3.0 s (the right one 10 ms later)
#include "run.h"
#include "avr_int.h"
#include "sim_inputs.h"
#include "../bumpers/bumpers.ino"

int main() {
  sim::din[4] = sim::bouncy_button({{1000, 1300}, {3000, 3400}});            // left bumper
  sim::din[7] = sim::bouncy_button({{2000, 2200}, {3010, 3400}});            // right bumper
  sim::run_ms(4000);
}
