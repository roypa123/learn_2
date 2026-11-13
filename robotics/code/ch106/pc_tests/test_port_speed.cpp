// test_port_speed.cpp - time 1000 pulses with digitalWrite and with PORTB
#include "run.h"
#include "avr_int.h"
#include "avr_regs.h"
#include "../port_speed/port_speed.ino"

int main() {
  sim::run_ms(100);
}
