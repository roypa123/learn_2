// test_rollover.cpp - start the clock 3.5 s before millis() wraps (49.7 days after power-on), run for 7 s
#include "run.h"
#include "avr_int.h"
#include "../rollover/rollover.ino"

int main() {
  sim::now_ns = (4294967296ULL - 3500ULL) * 1000000ULL;   // millis() starts at 4,294,963,796
  sim::run_ms(7000);
}
