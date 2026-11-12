// test_timer_bug.cpp - timer_bug.ino with the Uno's 16-bit int
#include "run.h"
#include "avr_int.h"
#include "../timer_bug/timer_bug.ino"

int main() {
  sim::run_ms(45000);
}
