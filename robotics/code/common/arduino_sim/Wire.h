// Wire.h - the Arduino I2C library on the PC test bench (Chapter 108)
//
// Simulated chips (see sim_i2c_devices.h) are put on the bus with sim::i2c_attach(address, &chip).
// Each transaction takes the time its bits really take at the bus speed (100 kHz unless setClock):
// a start, 9 bits for the address byte (8 bits + the acknowledge), 9 bits per data byte, and a stop.
// An address with no chip gives a "not acknowledged" result, as on a real bus.
// Not simulated: pull-ups, clock stretching, several controllers, errors on the wires.
#pragma once
#include "Arduino.h"
#include <map>

namespace sim {
struct I2CDevice {
    virtual ~I2CDevice() {}
    virtual void receive(const std::vector<uint8_t> &bytes) = 0;   // the data bytes of one write
    virtual uint8_t send() = 0;                                   // the next byte of a read
};
inline std::map<int, I2CDevice *> &i2c_bus() { static std::map<int, I2CDevice *> b; return b; }
inline void i2c_attach(int address, I2CDevice *d) { i2c_bus()[address] = d; }
inline uint32_t i2c_hz = 100000;
inline bool trace_i2c = false;                    // print every transaction
inline void i2c_bits(int n) { advance((uint64_t)n * 1000000000ULL / i2c_hz); }
}  // namespace sim

class TwoWire {
    int address = 0;
    std::vector<uint8_t> tx;
    std::deque<uint8_t> rx;

  public:
    void begin() {}
    void setClock(uint32_t hz) { sim::i2c_hz = hz; }
    void beginTransmission(int a) { address = a; tx.clear(); }
    size_t write(uint8_t b) {
        if (tx.size() >= 32) return 0;            // the real library's buffer holds 32 bytes
        tx.push_back(b);
        return 1;
    }
    size_t write(const uint8_t *buf, size_t n) { size_t k = 0; for (size_t i = 0; i < n; i++) k += write(buf[i]); return k; }
    uint8_t endTransmission(bool stop = true) {   // 0 = done, 2 = nobody answered the address
        (void)stop;
        auto it = sim::i2c_bus().find(address);
        if (it == sim::i2c_bus().end()) {
            sim::i2c_bits(1 + 9 + 1);
            if (sim::trace_i2c) std::printf("%sI2C write to 0x%02X: no answer\n", sim::stamp(), address);
            return 2;
        }
        sim::i2c_bits(1 + 9 * (1 + (int)tx.size()) + 1);
        if (sim::trace_i2c) {
            std::printf("%sI2C write to 0x%02X:", sim::stamp(), address);
            for (uint8_t b : tx) std::printf(" %02X", b);
            std::printf("\n");
        }
        it->second->receive(tx);
        return 0;
    }
    uint8_t requestFrom(int a, int n, int stop = 1) {
        (void)stop;
        rx.clear();
        auto it = sim::i2c_bus().find(a);
        if (it == sim::i2c_bus().end()) { sim::i2c_bits(1 + 9 + 1); return 0; }
        if (n > 32) n = 32;
        sim::i2c_bits(1 + 9 * (1 + n) + 1);
        for (int i = 0; i < n; i++) rx.push_back(it->second->send());
        if (sim::trace_i2c) {
            std::printf("%sI2C read from 0x%02X:", sim::stamp(), a);
            for (uint8_t b : rx) std::printf(" %02X", b);
            std::printf("\n");
        }
        return (uint8_t)n;
    }
    int available() { return (int)rx.size(); }
    int read() {
        if (rx.empty()) return -1;
        int b = rx.front();
        rx.pop_front();
        return b;
    }
};
inline TwoWire Wire;
