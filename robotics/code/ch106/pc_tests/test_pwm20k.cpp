// test_pwm20k.cpp - a "logic analyser" on pin 9: frequency and duty of each 0.2 s speed setting
#include "run.h"
#include "avr_int.h"
#include "avr_regs.h"
#include "../pwm20k/pwm20k.ino"

void measure() {                       // print what pin 9 did since the last call, then start again
  sim::Timer &t = sim::timer1;
  double seconds = t.an_ticks / 16e6;  // prescaler 1: one timer tick per clock cycle
  std::printf("   pin 9 measured: %.0f Hz, HIGH %.1f%% of the time\n",
              t.an_rises / seconds, 100.0 * t.an_high / t.an_ticks);
  t.an_ticks = t.an_high = t.an_rises = 0;
}

int main() {
  for (int k = 0; k < 5; k++) {        // speed changes at 200, 400, 600 and 800 ms
    sim::run_ms(k == 0 ? 199 : 197);   // measure from 2 ms after a change to 1 ms before the next
    measure();
    sim::run_ms(3);
    sim::timer1.an_ticks = sim::timer1.an_high = sim::timer1.an_rises = 0;
  }
}
