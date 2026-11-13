// test_shift_speed.cpp - a 74HC595 on pins 10 (latch), 11 (data) and 13 (clock); count what it latches
#include "run.h"
#include "avr_int.h"
#include "sim_spi_devices.h"
#include "../shift_speed/shift_speed.ino"

int main() {
  sim::HC595 chip(10, 11, 13);
  int latches = 0;
  uint8_t first = 0, last = 0;
  chip.on_latch = [&](uint8_t q) { if (latches++ == 0) first = q; last = q; };
  sim::spi_attach(&chip);
  sim::run_ms(100);
  std::printf("the 595 latched %d times; first Q7..Q0 = ", latches);
  for (int k = 7; k >= 0; k--) std::printf("%d", first >> k & 1);
  std::printf(", last Q7..Q0 = ");
  for (int k = 7; k >= 0; k--) std::printf("%d", last >> k & 1);
  std::printf("\n");
}
