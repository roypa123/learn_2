// test_break_millis.cpp - print the real (simulated) time in front of each line
#include "run.h"
#include "avr_int.h"
#include "avr_regs.h"
#include "../break_millis/break_millis.ino"

int main() {
  sim::serial_time = true;
  sim::run_ms(3200);
}
