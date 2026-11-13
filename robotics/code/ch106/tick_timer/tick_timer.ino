// tick_timer.ino - the same 100 Hz control step started by a Timer1 interrupt, with the same slow job
volatile unsigned long prevStart = 0;  // all shared with the ISR: volatile (Chapter 105)
volatile unsigned long minGap = 4000000000UL;
volatile unsigned long maxGap = 0;
volatile long steps = 0;
unsigned long lastSlow = 0;
unsigned long lastReport = 0;

void controlStep() {                   // exactly the same work as in tick_millis.ino
  unsigned long now = micros();
  if (steps > 0) {
    unsigned long gap = now - prevStart;
    if (gap < minGap) minGap = gap;
    if (gap > maxGap) maxGap = gap;
  }
  prevStart = now;
  steps++;
}

ISR(TIMER1_COMPA_vect) {               // 100 times per second, whatever loop() is doing
  controlStep();
}

void setup() {
  Serial.begin(115200);
  noInterrupts();
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;
  OCR1A = 19999;                       // 16,000,000 / 8 / 100 - 1 (timer_calc.py)
  TCCR1B = (1 << WGM12) | (1 << CS11); // CTC mode, prescaler 8
  TIMSK1 = (1 << OCIE1A);
  interrupts();
}

void loop() {
  if (millis() - lastSlow >= 35) {     // the same slow job
    lastSlow += 35;
    delayMicroseconds(6000);
  }
  if (millis() - lastReport >= 1000) {
    lastReport += 1000;
    noInterrupts();                    // copy the shared values in one piece
    long s = steps;
    unsigned long lo = minGap;
    unsigned long hi = maxGap;
    minGap = 4000000000UL;
    maxGap = 0;
    interrupts();
    Serial.print("steps: ");
    Serial.print(s);
    Serial.print("   gap between steps: ");
    Serial.print(lo);
    Serial.print(" to ");
    Serial.print(hi);
    Serial.println(" us");
  }
}
