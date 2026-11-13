// test_imu_tilt.cpp - Rover on the flat, then driving up onto a 15 degree ramp between 1.0 and 1.4 s.
// Driving adds a small vibration (0.02 g at 37 Hz) to the forward axis.
#include "run.h"
#include "avr_int.h"
#include "sim_i2c_devices.h"
#include "../imu_tilt/imu_tilt.ino"

int main() {
  sim::MPU6050 imu;
  imu.accel = [](double t, double &x, double &y, double &z) {
    double deg = t < 1.0 ? 0 : (t < 1.4 ? 15 * (t - 1.0) / 0.4 : 15);
    double a = deg * PI / 180;
    x = std::sin(a) + 0.02 * std::sin(2 * PI * 37 * t);
    y = 0;
    z = std::cos(a);
  };
  sim::i2c_attach(0x68, &imu);
  sim::run_ms(2050);
}
