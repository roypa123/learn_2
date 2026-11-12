// test_print_cost.cpp - print_cost.ino on the PC test bench (which models the 64-byte buffer and the baud rate)
#include "run.h"
#include "avr_int.h"
#include "../print_cost/print_cost.ino"

int main() {
  sim::run_ms(2000);
}
