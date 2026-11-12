// test_status_leds.cpp - status_leds.ino on the PC test bench, Uno int, every pin change printed
#include "run.h"
#include "avr_int.h"
#include "../status_leds/status_leds.ino"

int main() {
  sim::trace_pins = true;
  sim::serial_time = true;
  sim::run_ms(6000);
}
