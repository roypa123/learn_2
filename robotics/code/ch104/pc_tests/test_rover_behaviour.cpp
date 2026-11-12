// test_rover_behaviour.cpp - start at 0.5 s; a left bump at 2.0 s; both bumpers at 4.0 s (the right one
// 10 ms after the left); start pressed again at 7.0 s to stop. Every button bounces (sim_inputs.h).
#include "run.h"
#include "avr_int.h"
#include "sim_inputs.h"
#include "../rover_behaviour/rover_behaviour.ino"

int main() {
  sim::din[2] = sim::bouncy_button({{500, 700}, {7000, 7200}});     // start button
  sim::din[4] = sim::bouncy_button({{2000, 2200}, {4000, 4300}});   // left bumper
  sim::din[7] = sim::bouncy_button({{4010, 4300}});                 // right bumper
  sim::run_ms(8000);
}
