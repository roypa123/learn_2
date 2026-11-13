// tick_millis.ino - Rover's 100 Hz control step timed with millis() (Chapter 103), in a loop with a slow job
const unsigned long STEP_MS = 10;      // 100 control steps per second

unsigned long lastStep = 0;
unsigned long lastSlow = 0;
unsigned long lastReport = 0;
unsigned long prevStart = 0;           // when the previous control step started, in microseconds
unsigned long minGap = 4000000000UL;
unsigned long maxGap = 0;
long steps = 0;

void controlStep() {                   // the time-critical work: read the encoders, set the motors (Chapter 216)
  unsigned long now = micros();
  if (steps > 0) {
    unsigned long gap = now - prevStart;
    if (gap < minGap) minGap = gap;
    if (gap > maxGap) maxGap = gap;
  }
  prevStart = now;
  steps++;
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (millis() - lastStep >= STEP_MS) {
    lastStep += STEP_MS;
    controlStep();
  }
  if (millis() - lastSlow >= 35) {     // a slow job every 35 ms: sensors and messages that take 6 ms
    lastSlow += 35;
    delayMicroseconds(6000);
  }
  if (millis() - lastReport >= 1000) {
    lastReport += 1000;
    Serial.print("steps: ");
    Serial.print(steps);
    Serial.print("   gap between steps: ");
    Serial.print(minGap);
    Serial.print(" to ");
    Serial.print(maxGap);
    Serial.println(" us");
    minGap = 4000000000UL;
    maxGap = 0;
  }
}
