// test_delay_blind.cpp - eight quick presses (150 ms each) of the button on pin 2, during 8 seconds
#include "run.h"
#include "avr_int.h"
#include "presses.h"
#include "../delay_blind/delay_blind.ino"

int main() {
  sim::din[2] = eight_presses;
  sim::run_ms(8000);
}
