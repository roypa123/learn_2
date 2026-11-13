// sim_spi_devices.h - simulated SPI chips for the PC test bench (Chapter 109)
#pragma once
#include "SPI.h"
#include "sim_i2c_devices.h"                       // the MPU-6000 shares the MPU-6050's registers

namespace sim {
// 74HC595: an 8-bit shift register with an output latch.
// Bits go in on SER at each rising edge of SRCLK (the newest bit enters at Q0 and the others move up
// towards Q7); a rising edge on RCLK copies the shift register to the outputs Q0-Q7.
// It works with shiftOut() on any pins (data_pin, clock_pin) or with hardware SPI (MOSI and SCK),
// with RCLK used like a chip select: LOW while sending, and its rise latches the byte.
struct HC595 : SPIDevice {
    int data_pin = -1, clock_pin = -1;
    uint8_t shift = 0, out = 0;
    int last_clock = LOW, last_latch = LOW;
    std::function<void(uint8_t)> on_latch;         // called with the new outputs
    explicit HC595(int latch_pin, int data = -1, int clock = -1) : data_pin(data), clock_pin(clock) {
        cs = latch_pin;
        tick_hooks.push_back([this]() { watch(); });
    }
    void watch() {
        if (clock_pin >= 0) {
            int c = level[clock_pin];
            if (c == HIGH && last_clock == LOW) shift = (uint8_t)(shift << 1 | (level[data_pin] & 1));
            last_clock = c;
        }
        int l = level[cs];
        if (l == HIGH && last_latch == LOW) {
            out = shift;
            if (on_latch) on_latch(out);
        }
        last_latch = l;
    }
    uint8_t exchange(uint8_t b) override {         // SPI: 8 bits in; the 8 bits pushed out leave on Q7'
        uint8_t old = shift;
        shift = b;
        return old;
    }
};

// MPU-6000: the SPI version of the MPU-6050, with the same registers. The first byte after
// chip select goes LOW is the register number, with bit 7 = 1 for a read; the pointer then moves on
// by one for each following byte.
struct MPU6000 : SPIDevice {
    MPU6050 chip;                                  // the registers and the motion model
    bool fresh = true, reading = false;
    explicit MPU6000(int cs_pin) {
        cs = cs_pin;
        tick_hooks.push_back([this]() { if (level[cs] == HIGH) fresh = true; });
    }
    uint8_t exchange(uint8_t b) override {
        if (fresh) {                               // the register byte
            fresh = false;
            reading = b & 0x80;
            chip.ptr = b & 0x7F;
            if (reading) chip.sample();
            return 0x00;
        }
        if (reading) return chip.send();
        chip.reg[chip.ptr] = b;
        chip.ptr = (chip.ptr + 1) & 0x7F;
        return 0x00;
    }
};
}  // namespace sim
