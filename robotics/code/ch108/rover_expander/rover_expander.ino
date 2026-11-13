// rover_expander.ino - Rover's bumpers, status LED and buzzer on a PCF8574 I/O expander (I2C address 0x20)
#include <Wire.h>
const int EXPANDER = 0x20;
const byte LEFT_BUMPER = 0;            // P0: switch to GND, so LOW when pressed
const byte RIGHT_BUMPER = 1;           // P1: the same
const byte STATUS_LED = 4;             // P4: LED from 5 V through a resistor to the pin, so LOW = on
const byte BUZZER = 6;                 // P6: a buzzer module whose input is active LOW
byte outputs = 0xFF;                   // what we last wrote: 1 = HIGH (off, or an input), 0 = LOW (on)
byte lastBumpers = 0;
unsigned long lastPoll = 0;

void writeExpander() {
  Wire.beginTransmission(EXPANDER);
  Wire.write(outputs);                 // one byte sets all 8 pins at once
  Wire.endTransmission();
}

byte readExpander() {
  Wire.requestFrom(EXPANDER, 1);       // one byte gives all 8 pins at once
  return Wire.read();
}

void setOutput(byte bit, bool on) {    // "on" means LOW for these active-LOW parts
  if (on) {
    outputs &= ~(1 << bit);
  } else {
    outputs |= (1 << bit);
  }
  writeExpander();
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  writeExpander();                     // all HIGH: LED and buzzer off, bumper pins ready to be read
  setOutput(STATUS_LED, true);         // status LED on: "Rover is ready"
}

void loop() {
  if (millis() - lastPoll >= 10) {     // poll the bumpers 100 times per second (Chapter 99)
    lastPoll += 10;
    byte pins = readExpander();
    byte bumpers = 0;
    if (!(pins & (1 << LEFT_BUMPER))) bumpers |= 1;    // LOW = pressed
    if (!(pins & (1 << RIGHT_BUMPER))) bumpers |= 2;
    if (bumpers != lastBumpers) {
      lastBumpers = bumpers;
      setOutput(BUZZER, bumpers != 0);
      Serial.print(millis());
      Serial.print(" ms: bumpers ");
      Serial.print(bumpers & 1 ? "L" : "-");
      Serial.print(bumpers & 2 ? "R" : "-");
      Serial.println(bumpers ? "  buzzer on" : "  buzzer off");
    }
  }
}
