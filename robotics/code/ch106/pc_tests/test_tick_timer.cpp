// test_tick_timer.cpp - run the timer-interrupt control step for 3 seconds
#include "run.h"
#include "avr_int.h"
#include "avr_regs.h"
#include "../tick_timer/tick_timer.ino"

int main() {
  sim::run_ms(3050);
}
