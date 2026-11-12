// test_startup_beep.cpp - startup_beep.ino, with every tone() call printed
#include "run.h"
#include "avr_int.h"
#include "../startup_beep/startup_beep.ino"

int main() {
  sim::trace_pins = true;
  sim::run_ms(800);
}
