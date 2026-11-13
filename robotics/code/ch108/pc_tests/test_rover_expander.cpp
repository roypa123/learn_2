// test_rover_expander.cpp - left bumper pressed 0.30-0.80 s, both 1.00-1.20 s, right alone until 1.50 s.
// Every change of the expander's output pins is printed too.
#include "run.h"
#include "avr_int.h"
#include "sim_i2c_devices.h"
#include "sim_inputs.h"
#include "../rover_expander/rover_expander.ino"

int main() {
  sim::PCF8574 expander;
  expander.outside[0] = sim::bouncy_button({{300, 800}, {1000, 1200}});
  expander.outside[1] = sim::bouncy_button({{1000, 1500}});
  expander.on_change = [](uint8_t, uint8_t now) {
    std::printf("[%7.2f ms] expander pins: LED %s, buzzer %s\n", sim::t() * 1000,
                (now >> 4 & 1) ? "off" : "ON", (now >> 6 & 1) ? "off" : "ON");
  };
  sim::i2c_attach(0x20, &expander);
  sim::run_ms(1700);
}
