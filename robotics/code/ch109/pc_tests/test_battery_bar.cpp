// test_battery_bar.cpp - a battery that empties from 8.30 V to 6.10 V in 11 seconds (100s of times faster
// than a real one, to see every step), behind a 68 k / 10 k divider on A3
#include "run.h"
#include "avr_int.h"
#include "sim_spi_devices.h"
#include "../battery_bar/battery_bar.ino"

int main() {
  sim::HC595 chip(10);
  sim::spi_attach(&chip);
  sim::ain[A3] = [](double t) { return (8.30 - 0.20 * t) * 10.0 / 78.0; };
  sim::run_ms(11500);
}
