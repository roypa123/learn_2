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
// Run until simulated time reaches target_ns, but never stop in the middle of a pass of loop():
// a pass that is still running at the target finishes first (used by pipe_main.h, Chapter 111).
inline void run_until_ns(uint64_t target_ns) {
    if (!started) { started = true; setup(); }
    while (now_ns < target_ns) { loop(); advance(loop_ns); }
    std::fflush(stdout);
}
}  // namespace sim
