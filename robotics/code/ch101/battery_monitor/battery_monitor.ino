// battery_monitor.ino - read Rover's battery against the chip's own 1.1 V reference, so a sagging 5 V rail does not matter
const int BATTERY_PIN = A3;
const float REF_V = 1.1;               // the internal reference: about 1.1 V on every chip (calibrate it: Lab 101.2)
const float DIVIDER = 10.0 / 78.0;     // 68 k on top, 10 k below: the pin sees 10/78 of the battery
const int SAMPLES = 16;                // average 16 readings to cut the noise by 4 (Chapter 97)

float readBattery() {
  long sum = 0;
  for (int i = 0; i < SAMPLES; i++) {
    sum = sum + analogRead(BATTERY_PIN);
  }
  float count = sum / (float)SAMPLES;          // the average count, with decimals
  return count * REF_V / 1024 / DIVIDER;       // count -> volts on the pin -> volts of the battery
}

void setup() {
  Serial.begin(115200);
  analogReference(INTERNAL);           // compare with the 1.1 V reference instead of the 5 V rail
  analogRead(BATTERY_PIN);             // throw away the first reading after changing the reference
  delay(10);                           // and give the reference a moment to settle
}

void loop() {
  float volts = readBattery();
  Serial.print("battery ");
  Serial.print(volts, 2);
  Serial.print(" V  ");
  if (volts >= 7.2) {
    Serial.println("fine");
  } else if (volts >= 6.6) {
    Serial.println("low");
  } else {
    Serial.println("GO HOME");
  }
  delay(1000);
}
