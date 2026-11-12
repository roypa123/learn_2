// floating.ino - read a pin with NOTHING connected to it: what does it say?
const int PIN = 7;                     // leave pin 7 empty

void setup() {
  Serial.begin(9600);
  pinMode(PIN, INPUT);                 // a plain input: no pull-up, no pull-down
  for (int i = 0; i < 20; i++) {
    Serial.print(digitalRead(PIN));    // 1 or 0
    Serial.print(" ");
    delay(50);
  }
  Serial.println();
}

void loop() {
}
