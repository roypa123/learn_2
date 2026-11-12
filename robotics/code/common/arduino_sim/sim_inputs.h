// sim_inputs.h - ready-made pretend inputs for PC tests: buttons that bounce, pulse trains
#pragma once
#include <vector>
#include <functional>
#include "Arduino.h"

namespace sim {
struct Press {
    double down_ms, up_ms;                 // when the button is pressed and released
};

// A push button wired between the pin and GND, read with INPUT_PULLUP:
// HIGH when free, LOW when pressed. When the contacts close or open they bounce:
// the level changes 7 times during the first bounce_ms milliseconds.
inline std::function<int(double)> bouncy_button(std::vector<Press> presses, double bounce_ms = 3.0) {
    static const double edges[7] = {0.0, 0.08, 0.15, 0.35, 0.45, 0.70, 0.85};   // as fractions of bounce_ms
    return [=](double t) {
        double ms = t * 1000.0;
        for (const Press &p : presses) {
            if (ms >= p.down_ms && ms < p.up_ms) {             // pressing
                double x = (ms - p.down_ms) / bounce_ms;
                if (x >= 1.0) return LOW;
                int k = 0;
                while (k < 7 && edges[k] <= x) k++;
                return (k % 2 == 1) ? LOW : HIGH;
            }
            if (ms >= p.up_ms && ms < p.up_ms + bounce_ms) {   // releasing
                double x = (ms - p.up_ms) / bounce_ms;
                int k = 0;
                while (k < 7 && edges[k] <= x) k++;
                return (k % 2 == 1) ? HIGH : LOW;
            }
        }
        return HIGH;
    };
}
}  // namespace sim
