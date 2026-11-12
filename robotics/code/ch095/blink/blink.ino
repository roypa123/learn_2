// blink.ino - the classic first sketch: the board's LED on for one second, off for one second
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);        // pin 13 becomes an output
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);     // 5 V on pin 13: the LED lights
  delay(1000);                         // wait one second
  digitalWrite(LED_BUILTIN, LOW);      // 0 V on pin 13: the LED goes out
  delay(1000);
}
