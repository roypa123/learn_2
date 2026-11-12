// test_debounce_fsm.cpp - the same five bouncing presses as Chapter 99's test_debounce.cpp
#include "run.h"
#include "avr_int.h"
#include "sim_inputs.h"
#include "../debounce_fsm/debounce_fsm.ino"

int main() {
  sim::din[2] = sim::bouncy_button({{500, 700}, {1300, 1500}, {2100, 2300}, {2900, 3100}, {3700, 3900}});
  sim::run_ms(5100);
}
