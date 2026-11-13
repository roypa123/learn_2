// shift_speed.ino - send a byte to a 74HC595 shift register: with shiftOut() in software, then with hardware SPI
#include <SPI.h>
const int LATCH_PIN = 10;              // the 595's RCLK
const int DATA_PIN = 11;               // the 595's SER   (also SPI's MOSI pin)
const int CLOCK_PIN = 13;              // the 595's SRCLK (also SPI's SCK pin)

void writeShiftOut(byte pattern) {
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, pattern);   // 8 bits, one clock pulse each, made in software
  digitalWrite(LATCH_PIN, HIGH);       // the rising edge copies the 8 bits to the outputs
}

void writeSPI(byte pattern) {
  digitalWrite(LATCH_PIN, LOW);
  SPI.transfer(pattern);               // the same 8 bits and 8 clock pulses, made by the SPI hardware
  digitalWrite(LATCH_PIN, HIGH);
}

void setup() {
  Serial.begin(115200);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);

  unsigned long t0 = micros();
  for (int i = 0; i < 100; i++) {
    writeShiftOut(0b10110001);
  }
  unsigned long t1 = micros();

  SPI.begin();                         // from now on the SPI hardware drives pins 11 and 13
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));
  unsigned long t2 = micros();
  for (int i = 0; i < 100; i++) {
    writeSPI(0b10110001);
  }
  unsigned long t3 = micros();
  SPI.endTransaction();

  Serial.print("shiftOut: ");
  Serial.print((t1 - t0) / 100.0, 1);
  Serial.println(" us per update");
  Serial.print("SPI:      ");
  Serial.print((t3 - t2) / 100.0, 1);
  Serial.println(" us per update");
}

void loop() {
}
