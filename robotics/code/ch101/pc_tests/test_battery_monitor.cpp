// test_battery_monitor.cpp - the battery runs down from 8.4 V to 6.0 V in 8 s, and the 5 V rail sags with it
// (the Uno powered through VIN, as in Chapter 95), but the reading uses the internal 1.1 V reference
#include <cstdlib>
#include "run.h"
#include "avr_int.h"
#include "../battery_monitor/battery_monitor.ino"

double vbat(double t) { return 8.4 - 0.3 * t; }

int main() {
  if (getenv("CHIP_REF")) sim::internal_ref = atof(getenv("CHIP_REF"));   // this chip's real reference
  sim::vcc = [](double t) { return std::min(5.0, vbat(t) - 1.9); };
  sim::ain[A3] = [](double t) { return vbat(t) * 10.0 / 78.0; };
  sim::run_ms(8100);
}
