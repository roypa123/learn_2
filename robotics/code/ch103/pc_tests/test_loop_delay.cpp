// test_loop_delay.cpp - loop_delay.ino for 5 seconds, with 2.0 V on A0
#include "run.h"
#include "avr_int.h"
#include "../loop_delay/loop_delay.ino"

int main() {
  sim::ain[A0] = [](double t) { return 2.0; };
  sim::run_ms(5050);
}
