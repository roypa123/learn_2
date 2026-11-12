// test_multitask.cpp - multitask.ino for 3.1 s, with 2.5 V on A0
#include "run.h"
#include "avr_int.h"
#include "../multitask/multitask.ino"

int main() {
  sim::ain[A0] = [](double t) { return 2.5; };
  sim::run_ms(3100);
}
