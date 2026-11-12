// test_floating.cpp - nothing is connected to pin 7 (the bench gives random levels, like noise)
#include "run.h"
#include "avr_int.h"
#include "../floating/floating.ino"

int main() {
  sim::run_ms(1500);
}
