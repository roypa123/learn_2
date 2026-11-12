// test_fade.cpp - fade.ino for 2.1 seconds, printing every analogWrite that changes the pin
#include "run.h"
#include "avr_int.h"
#include "../fade/fade.ino"

int main() {
  sim::trace_pwm = true;
  sim::run_ms(2100);
}
