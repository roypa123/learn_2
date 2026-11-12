// run.h - runs a sketch on the PC test bench: setup() once, then loop() again and again
#pragma once
#include "Arduino.h"
void setup();
void loop();

namespace sim {
inline bool started = false;
// Run the sketch for this many milliseconds of simulated time.
inline void run_ms(double ms) {
    end_ns = now_ns + (uint64_t)(ms * 1e6);
    try {
        if (!started) { started = true; setup(); }
        while (true) { loop(); advance(loop_ns); }
    } catch (Stop &) {}
    end_ns = UINT64_MAX;
    std::fflush(stdout);
}
}  // namespace sim
