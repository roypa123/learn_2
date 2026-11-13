// break_millis.ino - what happens to millis() and delay() when a sketch changes Timer0 (do NOT do this)
void setup() {
  Serial.begin(115200);
  Serial.println("Timer0 as the Arduino core sets it (prescaler 64):");
  for (int i = 0; i < 3; i++) {
    delay(1000);
    Serial.println(millis());
  }
  TCCR0B = (TCCR0B & 0b11111000) | 0b001;   // Timer0 prescaler 64 -> 1, for 62.5 kHz PWM on pins 5 and 6
  Serial.println("after changing Timer0's prescaler to 1:");
  for (int i = 0; i < 3; i++) {
    delay(1000);
    Serial.println(millis());
  }
}

void loop() {
}
