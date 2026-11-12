// test_thermistor.cpp - the motor driver heats up from 25 C by 8 C per second; the supply is only 4.8 V;
// at 9.5 s the thermistor's wire breaks
#include <cmath>
#include "run.h"
#include "avr_int.h"
#include "../thermistor/thermistor.ino"

int main() {
  sim::vcc = [](double t) { return 4.8; };
  sim::ain[A1] = [](double t) {
    if (t >= 9.5) return 4.8;                                     // broken wire: the pin is pulled up to the supply
    double kelvin = 25 + 8 * t + 273.15;
    double r = 10000.0 * std::exp(3950.0 * (1.0 / kelvin - 1.0 / 298.15));
    return 4.8 * r / (1500.0 + r);
  };
  sim::run_ms(10500);
}
