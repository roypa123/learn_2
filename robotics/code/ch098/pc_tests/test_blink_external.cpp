// test_blink_external.cpp - blink_external.ino on the PC test bench, Uno int, every pin change printed
#include "run.h"
#include "avr_int.h"
#include "../blink_external/blink_external.ino"

int main() {
  sim::trace_pins = true;
  sim::serial_time = true;
  sim::run_ms(2100);
}
