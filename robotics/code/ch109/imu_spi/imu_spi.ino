// imu_spi.ino - read an MPU-6000 IMU over SPI (the SPI version of Chapter 108's MPU-6050), and time each reading
#include <SPI.h>
const int IMU_CS = 10;                 // the IMU's chip select
const SPISettings SLOW(1000000, MSBFIRST, SPI_MODE0);   // settings registers: at most 1 MHz (datasheet)
const SPISettings FAST(8000000, MSBFIRST, SPI_MODE0);   // measurements: up to 20 MHz; the Uno's top is 8 MHz
unsigned long lastRead = 0;

byte readRegister(byte reg) {
  SPI.beginTransaction(SLOW);
  digitalWrite(IMU_CS, LOW);           // select the IMU
  SPI.transfer(reg | 0x80);            // the register number, with bit 7 = 1 for "read"
  byte value = SPI.transfer(0);        // send anything: the chip's answer comes back at the same time
  digitalWrite(IMU_CS, HIGH);          // deselect
  SPI.endTransaction();
  return value;
}

void writeRegister(byte reg, byte value) {
  SPI.beginTransaction(SLOW);
  digitalWrite(IMU_CS, LOW);
  SPI.transfer(reg & 0x7F);            // bit 7 = 0 for "write"
  SPI.transfer(value);
  digitalWrite(IMU_CS, HIGH);
  SPI.endTransaction();
}

void setup() {
  Serial.begin(115200);
  pinMode(IMU_CS, OUTPUT);
  digitalWrite(IMU_CS, HIGH);          // not selected until we talk to it
  SPI.begin();
  Serial.print("WHO_AM_I = 0x");
  Serial.println(readRegister(0x75), HEX);
  writeRegister(0x6B, 0);              // wake up, as in Chapter 108
}

void loop() {
  if (millis() - lastRead >= 250) {
    lastRead += 250;
    byte raw[14];
    unsigned long t0 = micros();
    SPI.beginTransaction(FAST);
    digitalWrite(IMU_CS, LOW);
    SPI.transfer(0x3B | 0x80);         // start reading at ACCEL_XOUT_H
    for (int i = 0; i < 14; i++) {
      raw[i] = SPI.transfer(0);        // all 14 measurement bytes, one after another
    }
    digitalWrite(IMU_CS, HIGH);
    SPI.endTransaction();
    unsigned long t1 = micros();
    int16_t az = (int16_t)((raw[4] << 8) | raw[5]);     // acceleration Z: bytes 4 and 5
    int16_t gz = (int16_t)((raw[12] << 8) | raw[13]);   // rotation Z: bytes 12 and 13
    Serial.print(millis());
    Serial.print(" ms: z ");
    Serial.print(az / 16384.0, 3);
    Serial.print(" g, turning ");
    Serial.print(gz / 131.0, 1);       // 131 counts per degree per second (Chapter 96)
    Serial.print(" deg/s; the 14-byte read took ");
    Serial.print(t1 - t0);
    Serial.println(" us");
  }
}
