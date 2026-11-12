// test_loop_steady.cpp - loop_steady.ino for 5 seconds, with 2.0 V on A0
#include "run.h"
#include "avr_int.h"
#include "../loop_steady/loop_steady.ino"

int main() {
  sim::ain[A0] = [](double t) { return 2.0; };
  sim::run_ms(5050);
}
