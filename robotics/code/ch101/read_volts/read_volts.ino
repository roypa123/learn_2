// read_volts.ino - read the voltage on A0 and show it three ways: the raw count, volts, and millivolts
const int SENSOR_PIN = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int count = analogRead(SENSOR_PIN);  // 0 to 1023
  float volts = count * 5.0 / 1024;    // the count back into volts (the reference is 5 V)
  long mv = count * 5000L / 1024;      // whole millivolts with no float: 5000L makes it long maths
  int mvWrong = count * 5000 / 1024;   // WRONG: count * 5000 is done in int and overflows (Chapter 96)
  Serial.print(count);
  Serial.print(" counts = ");
  Serial.print(volts, 3);
  Serial.print(" V = ");
  Serial.print(mv);
  Serial.print(" mV   (int maths gives ");
  Serial.print(mvWrong);
  Serial.println(")");
  delay(500);
}
