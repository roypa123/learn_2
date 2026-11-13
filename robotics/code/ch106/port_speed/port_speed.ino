// port_speed.ino - how long do 1000 pulses on pin 13 take with digitalWrite, and with the port register?
void setup() {
  Serial.begin(115200);
  pinMode(13, OUTPUT);

  unsigned long t0 = micros();
  for (int i = 0; i < 1000; i++) {
    digitalWrite(13, HIGH);
    digitalWrite(13, LOW);
  }
  unsigned long t1 = micros();
  for (int i = 0; i < 1000; i++) {
    PORTB |= (1 << PB5);               // pin 13 is bit 5 of port B (Chapter 98): set it  -> HIGH
    PORTB &= ~(1 << PB5);              // clear it -> LOW
  }
  unsigned long t2 = micros();

  Serial.print("digitalWrite:  1000 pulses in ");
  Serial.print(t1 - t0);
  Serial.println(" us");
  Serial.print("PORTB:         1000 pulses in ");
  Serial.print(t2 - t1);
  Serial.println(" us");
}

void loop() {
}
