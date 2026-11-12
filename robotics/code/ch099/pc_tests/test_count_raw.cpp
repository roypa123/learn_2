// test_count_raw.cpp - five presses of 200 ms, each with 3 ms of contact bounce when pressed and when released
#include "run.h"
#include "avr_int.h"
#include "sim_inputs.h"
#include "../count_raw/count_raw.ino"

int main() {
  sim::din[2] = sim::bouncy_button({{500, 700}, {1300, 1500}, {2100, 2300}, {2900, 3100}, {3700, 3900}});
  sim::run_ms(5100);
}
