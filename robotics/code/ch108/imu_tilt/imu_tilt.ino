// imu_tilt.ino - read Rover's IMU (an MPU-6050) over I2C and work out how far Rover is tilted
#include <Wire.h>
const int IMU = 0x68;                  // the MPU-6050's address (its AD0 pin connected to GND)
const float COUNTS_PER_G = 16384.0;    // at the +-2 g range: 16,384 counts = 1 g
unsigned long lastRead = 0;

void writeRegister(byte reg, byte value) {
  Wire.beginTransmission(IMU);
  Wire.write(reg);                     // which register ...
  Wire.write(value);                   // ... and what to put in it
  Wire.endTransmission();
}

byte readRegister(byte reg) {
  Wire.beginTransmission(IMU);
  Wire.write(reg);                     // point at the register ...
  Wire.endTransmission(false);         // ... keep the bus (a "repeated start" follows) ...
  Wire.requestFrom(IMU, 1);            // ... and read one byte from it
  return Wire.read();
}

int16_t read16() {                     // two bytes, HIGH byte first, joined into one signed 16-bit number
  byte high = Wire.read();
  byte low = Wire.read();
  return (int16_t)((high << 8) | low);
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Serial.print("WHO_AM_I = 0x");
  Serial.println(readRegister(0x75), HEX);   // the chip's ID: 0x68 for an MPU-6050
  writeRegister(0x6B, 0);              // PWR_MGMT_1 = 0: wake up (the chip starts asleep)
}

void loop() {
  if (millis() - lastRead >= 200) {
    lastRead += 200;
    Wire.beginTransmission(IMU);
    Wire.write(0x3B);                  // ACCEL_XOUT_H: the first of the six acceleration bytes
    Wire.endTransmission(false);
    Wire.requestFrom(IMU, 6);          // X high, X low, Y high, Y low, Z high, Z low
    int16_t ax = read16();
    int16_t ay = read16();
    int16_t az = read16();
    float tilt = atan2(ax, az) * 180.0 / PI;   // nose up is positive (Chapter 47)
    Serial.print(millis());
    Serial.print(" ms: x ");
    Serial.print(ax);
    Serial.print("  y ");
    Serial.print(ay);
    Serial.print("  z ");
    Serial.print(az);
    Serial.print("  ->  x ");
    Serial.print(ax / COUNTS_PER_G, 3);
    Serial.print(" g, z ");
    Serial.print(az / COUNTS_PER_G, 3);
    Serial.print(" g, tilt ");
    Serial.print(tilt, 1);
    Serial.println(" deg");
  }
}
