// timer_bug.ino - a job that should run every 100 ms, timed with an int (wrong) and an unsigned long (right)
int lastBad = 0;                       // WRONG: millis() stops fitting in an int after 32.767 seconds
unsigned long lastGood = 0;            // right: the same type that millis() gives
long badRuns = 0;                      // how many times each job ran in the last 5 seconds
long goodRuns = 0;
unsigned long lastReport = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (millis() - lastBad >= 100) {     // is it 100 ms since the last time?
    lastBad = millis();
    badRuns++;
  }
  if (millis() - lastGood >= 100) {
    lastGood = millis();
    goodRuns++;
  }
  if (millis() - lastReport >= 5000) { // every 5 seconds, report and start counting again
    lastReport = millis();
    Serial.print(lastReport / 1000);
    Serial.print(" s: int timer ran ");
    Serial.print(badRuns);
    Serial.print(" times, unsigned long timer ran ");
    Serial.print(goodRuns);
    Serial.println(" times");
    badRuns = 0;
    goodRuns = 0;
  }
}
