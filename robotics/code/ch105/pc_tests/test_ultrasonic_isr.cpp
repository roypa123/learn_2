// test_ultrasonic_isr.cpp - a pretend HC-SR04 sensor: after each trigger pulse on pin 9 it waits 0.45 ms,
// then holds its echo pin (3) HIGH for the time sound takes to reach the wall and come back.
// The wall comes closer: 100 cm at t = 0, then 1 cm closer every 10 ms, until it is 40 cm away at t = 0.6 s.
#include "run.h"
#include "avr_int.h"
#include "../ultrasonic_isr/ultrasonic_isr.ino"

double trigFall = -1.0;                // when the trigger pin last went LOW, in seconds
int trigLast = LOW;

double wallCm(double t) { return t < 0.6 ? 100.0 - 100.0 * t : 40.0; }

int main() {
  sim::tick_hooks.push_back([]() {     // runs at every small time step: watch the trigger pin
    int now = sim::level[9];
    if (trigLast == HIGH && now == LOW) {
      trigFall = sim::t();
    }
    trigLast = now;
  });
  sim::din[3] = [](double t) {         // the echo pin
    if (trigFall < 0) {
      return LOW;
    }
    double start = trigFall + 0.00045;
    double width = wallCm(trigFall) * 2.0 / 34300.0;   // there and back, at 343 m/s
    return (t >= start && t < start + width) ? HIGH : LOW;
  };
  sim::run_ms(700);
}
