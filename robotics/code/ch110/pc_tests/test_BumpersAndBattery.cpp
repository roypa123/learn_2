// test_BumpersAndBattery.cpp - build RoverLib's example: the sketch, plus the library's two .cpp files.
// Left bumper pressed 200-400 ms and 900-1100 ms, right 600-700 ms, each with 3 ms of bounce;
// the battery is at 7.60 V.
// simrun-include: ../RoverLib/src
#include "run.h"
#include "avr_int.h"
#include "sim_inputs.h"
#include "../RoverLib/examples/BumpersAndBattery/BumpersAndBattery.ino"
#include "../RoverLib/src/Debouncer.cpp"
#include "../RoverLib/src/BatteryMonitor.cpp"

int main() {
  sim::din[4] = sim::bouncy_button({{200, 400}, {900, 1100}});
  sim::din[5] = sim::bouncy_button({{600, 700}});
  sim::ain[A3] = [](double) { return 7.60 * 10.0 / 78.0; };
  sim::run_ms(2050);
}
