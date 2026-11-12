// test_blink_millis.cpp - eight quick presses (150 ms each) of the button on pin 2, during 8 seconds
#include "run.h"
#include "avr_int.h"
#include "presses.h"
#include "../blink_millis/blink_millis.ino"

int main() {
  sim::din[2] = eight_presses;
  sim::run_ms(8000);
}
