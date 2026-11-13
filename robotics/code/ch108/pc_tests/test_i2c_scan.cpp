// test_i2c_scan.cpp - Rover's I2C bus: the I/O expander at 0x20 and the IMU at 0x68
#include "run.h"
#include "avr_int.h"
#include "sim_i2c_devices.h"
#include "../i2c_scan/i2c_scan.ino"

int main() {
  sim::PCF8574 expander;
  sim::MPU6050 imu;
  sim::i2c_attach(0x20, &expander);
  sim::i2c_attach(0x68, &imu);
  sim::run_ms(100);
}
