// test_commands.cpp - a person types seven commands into the Serial Monitor (line ending: Newline)
#include "run.h"
#include "avr_int.h"
#include "../commands/commands.ino"

int main() {
  sim::serial_time = true;
  sim::serial_send(500, "F 120\n");
  sim::serial_send(1500, "?\n");
  sim::serial_send(2500, "B 80\n");
  sim::serial_send(3500, "F\n");
  sim::serial_send(4500, "X 5\n");
  sim::serial_send(5500, "F 900\n");
  sim::serial_send(6500, "S\n");
  sim::run_ms(7000);
}
