// BatteryMonitor.cpp - how a BatteryMonitor does its work
#include "BatteryMonitor.h"

BatteryMonitor::BatteryMonitor(uint8_t pin, float rTop, float rBottom, float fullVolts, float emptyVolts) {
  _pin = pin;
  _ratio = rBottom / (rTop + rBottom);
  _full = fullVolts;
  _empty = emptyVolts;
}

void BatteryMonitor::begin() {
  analogReference(INTERNAL);
}

float BatteryMonitor::volts() {
  long sum = 0;
  for (int i = 0; i < 16; i++) {
    sum += analogRead(_pin);
  }
  return sum / 16.0 * 1.1 / 1024.0 / _ratio;
}

int BatteryMonitor::percent() {
  float p = (volts() - _empty) / (_full - _empty) * 100.0;
  return constrain((int)(p + 0.5), 0, 100);
}
