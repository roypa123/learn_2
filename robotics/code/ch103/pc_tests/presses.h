// presses.h - eight quick, clean presses of 150 ms on pin 2, used by two tests
#include "Arduino.h"
inline int eight_presses(double t) {
  static const double downs[8] = {700, 1650, 2400, 3300, 4150, 5050, 5800, 6900};
  double ms = t * 1000;
  for (double d : downs) {
    if (ms >= d && ms < d + 150) return LOW;
  }
  return HIGH;
}
