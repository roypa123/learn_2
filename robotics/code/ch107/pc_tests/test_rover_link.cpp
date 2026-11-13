// test_rover_link.cpp - play the Raspberry Pi: send motor packets (one damaged, one after some junk),
// then go quiet; decode and print every status packet the Arduino sends back.
#include "run.h"
#include "avr_int.h"
#include "../rover_link/rover_link.ino"

std::vector<uint8_t> packet(uint8_t type, std::vector<uint8_t> payload) {
  std::vector<uint8_t> p = {0xAA, (uint8_t)payload.size(), type};
  uint8_t s = (uint8_t)payload.size() + type;
  for (uint8_t b : payload) { p.push_back(b); s += b; }
  p.push_back(s);
  return p;
}
std::vector<uint8_t> motor(int16_t l, int16_t r) {
  return packet('M', {(uint8_t)(l & 0xFF), (uint8_t)((l >> 8) & 0xFF), (uint8_t)(r & 0xFF), (uint8_t)((r >> 8) & 0xFF)});
}
void pi_sends(double at_ms, const char *what, std::vector<uint8_t> bytes) {
  sim::run_ms(at_ms - sim::t() * 1000);
  std::printf("[%7.2f ms] Pi -> Arduino: %-26s", sim::t() * 1000, what);
  for (uint8_t b : bytes) std::printf(" %02X", b);
  std::printf("\n");
  sim::serial_send_bytes(at_ms, bytes);
}

std::vector<uint8_t> rx;                 // bytes from the Arduino, decoded packet by packet
void from_arduino(uint8_t b) {
  rx.push_back(b);
  if (rx[0] != 0xAA) { rx.clear(); return; }
  if (rx.size() < 2 || rx.size() < (size_t)rx[1] + 4) return;
  uint8_t s = 0;
  for (size_t i = 1; i + 1 < rx.size(); i++) s += rx[i];
  int16_t l = (int16_t)(rx[3] | rx[4] << 8), r = (int16_t)(rx[5] | rx[6] << 8);
  std::printf("[%7.2f ms] Arduino -> Pi: %c left %4d right %4d   good %d bad %d   (checksum %s)\n", sim::t() * 1000,
              rx[2], l, r, rx[7], rx[8], s == rx.back() ? "right" : "WRONG");
  rx.clear();
}

int main() {
  Serial.tx_hook = from_arduino;
  pi_sends(100, "M 120 120", motor(120, 120));
  pi_sends(300, "M 200 -80", motor(200, -80));
  std::vector<uint8_t> bad = motor(50, 50);
  bad[3] ^= 0x04;                        // noise flips one bit on the way
  pi_sends(500, "M 50 50, one bit flipped", bad);
  std::vector<uint8_t> junk = {'h', 'e', 'l', 'l', 'o'};
  for (uint8_t b : motor(60, 60)) junk.push_back(b);
  pi_sends(700, "junk, then M 60 60", junk);
  sim::run_ms(1300 - sim::t() * 1000);   // then the Pi says nothing more
}
