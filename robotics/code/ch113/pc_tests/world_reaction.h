// world_reaction.h - a pretend player for reaction_game.ino.
// The player watches the LED on pin 9: when it goes to full brightness (GO), they press the button on pin 2
// after their reaction time, and let go 150 ms later. In round 3 they lose patience and press 800 ms
// into the wait: a false start. Every press and release bounces for 3 ms (Chapter 99).
#pragma once
#include "Arduino.h"
#include <vector>

namespace world {
struct Press { double down, up; };
std::vector<Press> presses;
const double REACTION_MS[] = {231.4, 198.0, 264.7, 187.3, 243.9};
int go_count = 0, glow_count = 0;
bool was_go = false, was_glow = false;

int level_at(double t) {                   // the button pin: HIGH when free, LOW when pressed, with bounce
    static const double edges[7] = {0.0, 0.08, 0.15, 0.35, 0.45, 0.70, 0.85};
    double ms = t * 1000.0;
    for (const Press &p : presses) {
        for (int phase = 0; phase < 2; phase++) {
            double start = phase == 0 ? p.down : p.up;
            double x = (ms - start) / 3.0;
            if (x >= 0 && x < 1) {
                int k = 0;
                while (k < 7 && edges[k] <= x) k++;
                bool closed = (k % 2 == 1) == (phase == 0);
                return closed ? LOW : HIGH;
            }
        }
        if (ms >= p.down + 3.0 && ms < p.up) return LOW;
    }
    return HIGH;
}

void watch() {                             // runs at every simulated microsecond
    double ms = sim::t() * 1000.0;
    bool go = sim::level[9] == HIGH && sim::pwm[9] < 0;
    bool glow = sim::pwm[9] == 15;
    if (glow && !was_glow) {               // a new round's wait has begun
        glow_count++;
        if (glow_count == 3) presses.push_back({ms + 800, ms + 950});
    }
    if (go && !was_go) {                   // GO: react after this player's reaction time
        double r = REACTION_MS[go_count % 5];
        go_count++;
        presses.push_back({ms + r, ms + r + 150});
    }
    was_go = go;
    was_glow = glow;
}
}  // namespace world

void world_setup() {
    sim::din[2] = world::level_at;
    sim::ain[A0] = [](double) { return 2.37; };   // the "noise" on A0, fixed so every run is the same
    sim::tick_hooks.push_back(world::watch);
}
