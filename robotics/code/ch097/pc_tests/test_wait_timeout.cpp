// test_wait_timeout.cpp - run wait_timeout.ino twice: button pressed at 1.234 s, and never pressed
#include "run.h"
#include "avr_int.h"
#include "../wait_timeout/wait_timeout.ino"

int main() {
  const char *which = getenv("NEVER");
  if (which) {
    sim::din[2] = [](double t) { return HIGH; };         // nobody presses the button
  } else {
    sim::din[2] = [](double t) { return t < 1.234 ? HIGH : LOW; };   // pressed at 1.234 s
  }
  sim::run_ms(5000);
}
