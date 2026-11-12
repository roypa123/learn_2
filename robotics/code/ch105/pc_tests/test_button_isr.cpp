// test_button_isr.cpp - the five bouncing presses of Chapter 99, counted by an interrupt
#include "run.h"
#include "avr_int.h"
#include "sim_inputs.h"
#include "../button_isr/button_isr.ino"

int main() {
  sim::din[2] = sim::bouncy_button({{500, 700}, {1300, 1500}, {2100, 2300}, {2900, 3100}, {3700, 3900}});
  sim::run_ms(5100);
}
