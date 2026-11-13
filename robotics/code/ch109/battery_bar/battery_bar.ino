// battery_bar.ino - Rover's battery level on a bar of 8 LEDs, driven by a 74HC595 over SPI
#include <SPI.h>
const int LATCH_PIN = 10;              // the 595's RCLK, used like a chip select
const int BATTERY_PIN = A3;            // the battery through 68 k / 10 k (Chapter 101)
const float FULL = 8.4;                // volts
const float EMPTY = 6.0;
unsigned long lastUpdate = 0;
byte shown = 0;                        // the pattern the LEDs show now

float batteryVolts() {                 // Chapter 101's battery monitor: 16 readings, internal 1.1 V reference
  long sum = 0;
  for (int i = 0; i < 16; i++) {
    sum += analogRead(BATTERY_PIN);
  }
  float count = sum / 16.0;
  return count * 1.1 / 1024.0 / (10.0 / 78.0);
}

byte barPattern(float volts) {         // how many LEDs, as a pattern of 1s from the bottom
  int leds = (int)((volts - EMPTY) / (FULL - EMPTY) * 8 + 0.5);   // 0 to 8, rounded
  leds = constrain(leds, 0, 8);
  return (byte)((1 << leds) - 1);      // 3 LEDs: (1 << 3) - 1 = 8 - 1 = 0b00000111
}

void showBar(byte pattern) {
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));
  digitalWrite(LATCH_PIN, LOW);
  SPI.transfer(pattern);
  digitalWrite(LATCH_PIN, HIGH);       // the new pattern appears on the LEDs, all 8 at once
  SPI.endTransaction();
  shown = pattern;
}

void setup() {
  Serial.begin(115200);
  analogReference(INTERNAL);
  pinMode(LATCH_PIN, OUTPUT);
  SPI.begin();
  showBar(0);
}

void loop() {
  if (millis() - lastUpdate >= 1000) {
    lastUpdate += 1000;
    float v = batteryVolts();
    byte bar = barPattern(v);
    if (bar != shown) {
      showBar(bar);                    // only talk to the 595 when the picture changes
    }
    Serial.print(millis() / 1000);
    Serial.print(" s: ");
    Serial.print(v, 2);
    Serial.print(" V  [");
    for (int k = 7; k >= 0; k--) {     // draw the bar: Q7 on the left, Q0 on the right
      Serial.print((shown >> k) & 1 ? "#" : ".");
    }
    Serial.println("]");
  }
}
