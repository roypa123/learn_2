// test_sos.cpp - sos.ino on the PC test bench, Uno int, every pin change printed
#include "run.h"
#include "avr_int.h"
#include "../sos/sos.ino"

int main() {
  sim::trace_pins = true;
  sim::serial_time = true;
  sim::run_ms(7000);
}
