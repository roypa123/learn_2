// encoder_isr.ino - count the same pulses with an INTERRUPT, in a loop with exactly the same other work
const int ENC_A = 2;

volatile long count = 0;               // shared with the ISR
unsigned long lastReport = 0;

void onPulse() {                       // runs at every rising edge, whatever loop() is doing
  count++;
}

void setup() {
  Serial.begin(115200);
  pinMode(ENC_A, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENC_A), onPulse, RISING);
}

void loop() {
  delayMicroseconds(800);              // the same other work as in encoder_poll.ino
  if (millis() - lastReport >= 1000) {
    lastReport += 1000;
    noInterrupts();
    long copy = count;                 // a safe copy of the 4-byte count
    interrupts();
    Serial.print("pulses counted: ");
    Serial.println(copy);
  }
}
