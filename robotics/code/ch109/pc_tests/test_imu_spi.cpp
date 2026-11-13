// test_imu_spi.cpp - an MPU-6000 on chip select 10; the drone is level, and yaws at 90 deg/s from 0.5 to 1.0 s
#include "run.h"
#include "avr_int.h"
#include "sim_spi_devices.h"
#include "../imu_spi/imu_spi.ino"

int main() {
  sim::MPU6000 imu(10);
  imu.chip.gyro = [](double t, double &x, double &y, double &z) { x = 0; y = 0; z = (t >= 0.5 && t < 1.0) ? 90 : 0; };
  sim::spi_attach(&imu);
  sim::run_ms(1300);
}
