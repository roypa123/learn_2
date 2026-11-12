// encoder_wave.h - a clean encoder channel: a square wave at 1,305 Hz (Rover's wheel at 0.5 m/s, Chapter 94)
#include <cmath>
#include "Arduino.h"
inline int encoder_a(double t) {
  double phase = 1305.0 * t;
  return (phase - std::floor(phase)) < 0.5 ? LOW : HIGH;   // LOW for the first half of each pulse
}
