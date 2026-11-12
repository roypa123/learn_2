// test_heartbeat.cpp - run heartbeat.ino on the PC test bench for 2 seconds
#include "run.h"
#include "../heartbeat/heartbeat.ino"

int main() {
  sim::trace_pins = true;
  sim::run_ms(2000);
}
