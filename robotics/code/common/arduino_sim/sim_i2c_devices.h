// sim_i2c_devices.h - simulated I2C chips for the PC test bench (Chapter 108)
#pragma once
#include "Wire.h"
#include <cmath>

namespace sim {
// PCF8574: an 8-bit I/O expander. Each pin is "quasi-bidirectional": writing 0 pulls it LOW
// strongly (it can sink LED current); writing 1 leaves it HIGH through a weak pull-up, so it can
// also be read as an input, and something outside (a switch to ground) can pull it LOW.
struct PCF8574 : I2CDevice {
    uint8_t latch = 0xFF;                          // at power-on every pin is HIGH (weak)
    std::function<int(double)> outside[8];         // what pulls each pin LOW from outside, if anything
    std::function<void(uint8_t, uint8_t)> on_change;   // called with (old, new) when the outputs change
    void receive(const std::vector<uint8_t> &bytes) override {
        for (uint8_t b : bytes) {
            uint8_t old = latch;
            latch = b;
            if (old != b && on_change) on_change(old, b);
        }
    }
    uint8_t send() override {
        uint8_t v = 0;
        for (int k = 0; k < 8; k++) {
            int level = (latch >> k) & 1;          // 0: driven LOW by the chip
            if (level && outside[k] && outside[k](t()) == LOW) level = 0;
            v |= level << k;
        }
        return v;
    }
};

// MPU-6050: a 6-axis IMU (Chapters 125 and 127). Registers are read and written through a pointer
// that moves on by one after every byte. At power-on the chip is ASLEEP (PWR_MGMT_1 = 0x40) and its
// measurement registers read 0 until the sketch wakes it. Range: +-2 g (16,384 per g) and
// +-250 deg/s (131 per deg/s). 16-bit values are stored HIGH byte first.
struct MPU6050 : I2CDevice {
    uint8_t reg[128] = {0};
    uint8_t ptr = 0;
    // the motion: acceleration in g and rotation rate in deg/s, as functions of time
    std::function<void(double, double &, double &, double &)> accel = [](double, double &x, double &y, double &z) { x = 0; y = 0; z = 1; };
    std::function<void(double, double &, double &, double &)> gyro = [](double, double &x, double &y, double &z) { x = 0; y = 0; z = 0; };
    double temp_c = 25.0;
    MPU6050() { reg[0x75] = 0x68; reg[0x6B] = 0x40; }
    static void put16(uint8_t *r, double v) {
        long n = lround(v);
        if (n > 32767) n = 32767;
        if (n < -32768) n = -32768;
        uint16_t u = (uint16_t)(int16_t)n;
        r[0] = u >> 8;
        r[1] = u & 0xFF;
    }
    void sample() {                                // fill the measurement registers 0x3B to 0x48
        if (reg[0x6B] & 0x40) { for (int a = 0x3B; a <= 0x48; a++) reg[a] = 0; return; }   // asleep
        double ax, ay, az, gx, gy, gz;
        accel(t(), ax, ay, az);
        gyro(t(), gx, gy, gz);
        put16(&reg[0x3B], ax * 16384); put16(&reg[0x3D], ay * 16384); put16(&reg[0x3F], az * 16384);
        put16(&reg[0x41], (temp_c - 36.53) * 340);
        put16(&reg[0x43], gx * 131); put16(&reg[0x45], gy * 131); put16(&reg[0x47], gz * 131);
    }
    void receive(const std::vector<uint8_t> &bytes) override {
        if (bytes.empty()) return;
        ptr = bytes[0] & 0x7F;                     // the first byte chooses the register
        for (size_t i = 1; i < bytes.size(); i++) { reg[ptr] = bytes[i]; ptr = (ptr + 1) & 0x7F; }
        if (bytes.size() == 1) sample();           // about to be read: take a fresh measurement
    }
    uint8_t send() override {
        uint8_t v = reg[ptr];
        ptr = (ptr + 1) & 0x7F;
        return v;
    }
};
}  // namespace sim
