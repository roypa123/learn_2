// test_blink.cpp - run blink.ino on the PC test bench for 4.5 seconds
#include "run.h"
#include "../blink/blink.ino"

int main() {
  sim::trace_pins = true;
  sim::run_ms(4500);
}
