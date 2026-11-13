// test_timer1_blink.cpp - show every change of pin 13 for 3 seconds, while loop() sits in delay(3000)
#include "run.h"
#include "avr_int.h"
#include "avr_regs.h"
#include "../timer1_blink/timer1_blink.ino"

int main() {
  sim::trace_pins = true;
  sim::run_ms(3000);
}
