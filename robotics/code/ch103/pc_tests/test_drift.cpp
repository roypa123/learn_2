// test_drift.cpp - drift.ino for 10.5 s
#include "run.h"
#include "avr_int.h"
#include "../drift/drift.ino"

int main() {
  sim::run_ms(10500);
}
