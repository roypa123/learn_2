// BatteryMonitor.h - a battery's voltage through a resistor divider, against the 1.1 V internal reference (Chapter 101)
#pragma once
#include <Arduino.h>

class BatteryMonitor {
  public:
    BatteryMonitor(uint8_t pin, float rTop, float rBottom, float fullVolts = 8.4, float emptyVolts = 6.0);
    void begin();                      // switches the ADC to the 1.1 V reference
    float volts();                     // 16 readings, averaged
    int percent();                     // 0 to 100, straight line from empty to full

  private:
    uint8_t _pin;
    float _ratio;                      // rBottom / (rTop + rBottom)
    float _full;
    float _empty;
};
