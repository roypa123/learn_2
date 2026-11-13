// test_soft_tx_naive.cpp - a "logic analyser" with a serial decoder on each pin: pin 4 at 9600 baud, pin 5 at 19200
#include "run.h"
#include "avr_int.h"
#include "sim_probe.h"
#include "../soft_tx_naive/soft_tx_naive.ino"

std::string shown(const std::string &t) {          // bytes that cannot be printed are shown as \xNN
  std::string r;
  char buf[8];
  for (unsigned char c : t) {
    if (c >= 32 && c < 127) r += (char)c;
    else { std::snprintf(buf, sizeof buf, "\\x%02X", c); r += buf; }
  }
  return r;
}

int main() {
  sim::UartSniffer on4(4, 9600), on5(5, 19200);
  sim::run_ms(50);
  std::printf("pin 4 at  9600 baud decodes: \"%s\"   (framing errors: %d)\n", shown(on4.text).c_str(), on4.framing_errors);
  std::printf("pin 5 at 19200 baud decodes: \"%s\"   (framing errors: %d)\n", shown(on5.text).c_str(), on5.framing_errors);
}
