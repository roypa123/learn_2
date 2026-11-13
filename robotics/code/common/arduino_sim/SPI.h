// SPI.h - the Arduino SPI library on the PC test bench (Chapter 109)
//
// Simulated chips (see sim_spi_devices.h) each have a chip-select pin. SPI.transfer(b) exchanges one
// byte with the chip whose chip-select pin the sketch has made LOW (an OUTPUT driven LOW), and takes
// 8 clock periods plus about 0.8 us of the library's own work, as on a real Uno. The Uno's SPI clock
// is at most 8 MHz (16 MHz / 2). With no chip selected, MISO floats HIGH and the byte read is 0xFF.
// Not simulated: SPI modes (every chip here uses mode 0), bit order LSBFIRST, errors on the wires.
#pragma once
#include "Arduino.h"

#define SPI_MODE0 0x00
#define SPI_MODE1 0x04
#define SPI_MODE2 0x08
#define SPI_MODE3 0x0C

struct SPISettings {
    uint32_t clock;
    uint8_t order, mode;
    SPISettings(uint32_t c = 4000000, uint8_t o = MSBFIRST, uint8_t m = SPI_MODE0) : clock(c), order(o), mode(m) {}
};

namespace sim {
struct SPIDevice {
    int cs = -1;                                  // its chip-select pin on the Uno
    virtual ~SPIDevice() {}
    virtual uint8_t exchange(uint8_t mosi) = 0;   // one byte in from MOSI, one byte out on MISO
};
inline std::vector<SPIDevice *> &spi_devices() { static std::vector<SPIDevice *> d; return d; }
inline void spi_attach(SPIDevice *d) { spi_devices().push_back(d); }
inline uint32_t spi_hz = 4000000;
}  // namespace sim

class SPIClass {
  public:
    void begin() {                                // SCK (13), MOSI (11) and SS (10) become outputs
        pinMode(13, OUTPUT);
        pinMode(11, OUTPUT);
        pinMode(10, OUTPUT);
        digitalWrite(10, HIGH);
    }
    void beginTransaction(SPISettings s) {
        uint32_t hz = 8000000;                    // the Uno divides 16 MHz by 2, 4, 8 ... 128
        while (hz > s.clock && hz > 125000) hz /= 2;
        sim::spi_hz = hz;
    }
    void endTransaction() {}
    uint8_t transfer(uint8_t b) {
        sim::advance((uint64_t)8 * 1000000000ULL / sim::spi_hz + 800);
        uint8_t in = 0xFF;
        for (sim::SPIDevice *d : sim::spi_devices())
            if (d->cs >= 0 && sim::mode[d->cs] == OUTPUT && sim::level[d->cs] == LOW) in = d->exchange(b);
        return in;
    }
    void transfer(void *buf, size_t n) {
        uint8_t *p = (uint8_t *)buf;
        for (size_t i = 0; i < n; i++) p[i] = transfer(p[i]);
    }
};
inline SPIClass SPI;
