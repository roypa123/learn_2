// drift.ino - two "every 100 ms" jobs in a loop that is busy for 7 ms per pass:
// one remembers when it RAN (last = millis()), the other when it was DUE (last += 100)
const unsigned long INTERVAL = 100;

unsigned long lastA = 0;               // job A: last = millis()
unsigned long lastB = 0;               // job B: last += INTERVAL
long runsA = 0;
long runsB = 0;
bool reported = false;

void setup() {
  Serial.begin(115200);
}

void loop() {
  delay(7);                            // pretend the rest of the loop takes 7 ms (reading sensors, ...)
  if (millis() - lastA >= INTERVAL) {
    lastA = millis();                  // A: the next run is due 100 ms after this one RAN (late)
    runsA++;
  }
  if (millis() - lastB >= INTERVAL) {
    lastB += INTERVAL;                 // B: the next run is due 100 ms after this one was DUE
    runsB++;
  }
  if (!reported && millis() >= 10000) {     // after 10 s, report once (fine here: far from the wrap)
    reported = true;
    Serial.print("after 10 s: A ran ");
    Serial.print(runsA);
    Serial.print(" times, B ran ");
    Serial.print(runsB);
    Serial.println(" times (100 expected)");
  }
}
