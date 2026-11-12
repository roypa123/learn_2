// test_traffic_light.cpp - traffic_light.ino for 13 seconds
#include "run.h"
#include "avr_int.h"
#include "../traffic_light/traffic_light.ino"

int main() {
  sim::run_ms(13000);
}
