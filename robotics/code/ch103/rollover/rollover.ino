// rollover.ino - two once-a-second timers, across the moment millis() wraps from 4,294,967,295 back to 0
unsigned long lastSafe = 0;            // the safe way: subtract, then compare
unsigned long nextUnsafe = 0;          // the unsafe way: compare the time with a "due" time
long unsafeRuns = 0;

void setup() {
  Serial.begin(115200);
  lastSafe = millis();
  nextUnsafe = millis() + 1000;
}

void loop() {
  if (millis() >= nextUnsafe) {        // WRONG: fails when nextUnsafe has wrapped and millis() has not yet
    nextUnsafe += 1000;
    unsafeRuns++;
  }
  if (millis() - lastSafe >= 1000) {   // right, even across the wrap
    lastSafe += 1000;
    Serial.print("millis ");
    Serial.print(millis());
    Serial.print(": safe timer ran once; unsafe timer ran ");
    Serial.print(unsafeRuns);
    Serial.println(" times");
    unsafeRuns = 0;
  }
}
