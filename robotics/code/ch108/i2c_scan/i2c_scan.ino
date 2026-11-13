// i2c_scan.ino - ask every I2C address "is anyone there?" and list the chips that answer
#include <Wire.h>

void setup() {
  Serial.begin(115200);
  Wire.begin();                        // join the bus as the controller (pins A4 = SDA, A5 = SCL)
  Serial.println("scanning addresses 1 to 126 ...");
  int found = 0;
  for (int address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte result = Wire.endTransmission();   // 0: a chip answered (acknowledged) its address
    if (result == 0) {
      Serial.print("  chip found at 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      found++;
    }
  }
  Serial.print(found);
  Serial.print(" chip(s) found; the scan took ");
  Serial.print(millis());
  Serial.println(" ms");
}

void loop() {
}
