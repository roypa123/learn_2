// sim_probe.h - measuring instruments for PC tests (Chapter 110)
//
// UartSniffer: a receiver on any output pin, like a logic analyser that decodes serial.
// It waits for a falling edge (a start bit), then reads the pin in the middle of each bit,
// 1.5, 2.5 ... 8.5 bit-times later, with an exact clock at the baud rate it is given, and checks
// the stop bit at 9.5. It records each byte, and marks framing errors with '~'.
#pragma once
#include "Arduino.h"
#include <string>

namespace sim {
struct UartSniffer {
    int pin;
    double bit_s;
    std::string text;                              // decoded characters ('~' = framing error)
    int framing_errors = 0;
    bool busy = false;
    double start = 0;
    int k = 0, value = 0, last = HIGH;
    UartSniffer(int p, double baud) : pin(p), bit_s(1.0 / baud) {
        last = level[p];                           // a line that starts LOW is not a start bit
        tick_hooks.push_back([this]() { watch(); });
    }
    void watch() {
        int v = level[pin];
        double now = t();
        if (!busy) {
            if (last == HIGH && v == LOW) { busy = true; start = now; k = 0; value = 0; }
        } else {
            while (busy && now >= start + (k + 1.5) * bit_s) {
                if (k < 8) value |= v << k;
                else {
                    if (v == HIGH) text += (char)value;
                    else { text += '~'; framing_errors++; }
                    busy = false;
                }
                k++;
            }
        }
        last = v;
    }
};
}  // namespace sim
