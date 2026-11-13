// world_stream.h - the pretend world for sensor_stream.ino: a joint swinging between 45 and 225 degrees,
// once every 2 seconds, read by a 270-degree potentiometer powered from 5 V
#pragma once
#include "Arduino.h"

void world_setup() {
  sim::ain[A0] = [](double t) {
    double angle = 135.0 + 90.0 * std::sin(2.0 * PI * 0.5 * t);
    return angle / 270.0 * 5.0;
  };
}
