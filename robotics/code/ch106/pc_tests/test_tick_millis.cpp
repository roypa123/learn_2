// test_tick_millis.cpp - run the millis()-timed control step for 3 seconds
#include "run.h"
#include "avr_int.h"
#include "../tick_millis/tick_millis.ino"

int main() {
  sim::run_ms(3050);
}
