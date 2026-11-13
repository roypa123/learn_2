// test_traffic_light.cpp - a pedestrian presses at 3 s, again (impatiently) at 4 s, during the walk at 13 s,
// and once more at 30 s; each press has 3 ms of contact bounce. 50 seconds of traffic.
// simrun-include: ../../ch110/RoverLib/src
#include "run.h"
#include "avr_int.h"
#include "sim_inputs.h"
#include "../traffic_light/traffic_light.ino"
#include "../../ch110/RoverLib/src/Debouncer.cpp"

int main() {
  sim::din[12] = sim::bouncy_button({{3000, 3200}, {4000, 4150}, {13000, 13200}, {30000, 30300}});
  sim::run_ms(50000);
}
