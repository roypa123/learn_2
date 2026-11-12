// test_button_basic.cpp - the button is pressed from 0.25 s to 0.55 s
#include "run.h"
#include "avr_int.h"
#include "sim_inputs.h"
#include "../button_basic/button_basic.ino"

int main() {
  sim::din[2] = sim::bouncy_button({{250, 550}});
  sim::run_ms(800);
}
