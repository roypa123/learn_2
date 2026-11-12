// test_encoder_poll.cpp - Rover's encoder at 0.5 m/s (1,305 pulses per second) for 3 seconds
#include "run.h"
#include "avr_int.h"
#include "encoder_wave.h"
#include "../encoder_poll/encoder_poll.ino"

int main() {
  sim::din[2] = encoder_a;
  sim::run_ms(3050);
}
