// quadrature.ino - count Rover's wheel position, forwards AND backwards, from an encoder's two channels
const int ENC_A = 2;                   // channel A: on an interrupt pin
const int ENC_B = 4;                   // channel B: any digital pin
const float MM_PER_PULSE = 207.0 / 540;   // one wheel turn = 207 mm = 540 pulses (Chapters 16 and 47)

volatile long position = 0;            // in pulses: forwards adds, backwards subtracts
unsigned long lastReport = 0;

void onA() {                           // at each rising edge of A, B tells us the direction
  if (digitalRead(ENC_B) == LOW) {
    position++;                        // B still LOW: A is ahead of B, the wheel turns forwards
  } else {
    position--;                        // B already HIGH: B is ahead, the wheel turns backwards
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(ENC_A, INPUT_PULLUP);
  pinMode(ENC_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENC_A), onA, RISING);
}

void loop() {
  if (millis() - lastReport >= 500) {
    lastReport += 500;
    noInterrupts();
    long p = position;
    interrupts();
    Serial.print(millis());
    Serial.print(" ms: position ");
    Serial.print(p);
    Serial.print(" pulses = ");
    Serial.print(p * MM_PER_PULSE, 1);
    Serial.println(" mm");
  }
}
