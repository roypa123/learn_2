// test_hello_rover.cpp - run hello_rover.ino on the PC test bench for 3.2 seconds
#include "run.h"
#include "../hello_rover/hello_rover.ino"

int main() {
  sim::trace_pins = true;      // show every change of an output pin, with the time
  sim::serial_time = true;     // show the time in front of each line the sketch prints
  sim::run_ms(3200);
}
