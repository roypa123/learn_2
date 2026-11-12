// loop_steady.ino - a real 100 Hz control loop: start each step exactly 10,000 us after the last one was DUE
const int SENSOR_PIN = A0;
const unsigned long PERIOD_US = 10000; // 10 ms = 100 steps per second

unsigned long nextStart = 0;           // when the next step is due, in micros()
long loops = 0;
int reading = 0;                       // the latest averaged sensor reading
long overruns = 0;                     // steps that finished after the next one was due
unsigned long worstLate = 0;           // the latest a step has started, in microseconds

void controlStep() {                   // the same work as loop_delay.ino: about 2.2 ms
  long sum = 0;
  for (int i = 0; i < 20; i++) {
    sum += analogRead(SENSOR_PIN);
  }
  reading = sum / 20;
  if (loops % 250 == 125) {
    delay(12);                         // twice in 5 s, something takes much longer (12 ms more)
  }
}

void setup() {
  Serial.begin(115200);
  nextStart = micros();
}

void loop() {
  if ((long)(micros() - nextStart) >= 0) {        // is the next step due yet? (safe across the wrap)
    unsigned long late = micros() - nextStart;    // how late this step starts
    if (late > worstLate) {
      worstLate = late;
    }
    nextStart += PERIOD_US;                       // the following step is due one period after THIS one was due
    controlStep();
    loops++;
    if ((long)(micros() - nextStart) >= 0) {      // already past the next start time: an overrun
      overruns++;
    }
    if (loops % 100 == 0) {
      Serial.print(loops);
      Serial.print(" steps done at ");
      Serial.print(millis());
      Serial.print(" ms; overruns ");
      Serial.print(overruns);
      Serial.print(", latest start ");
      Serial.print(worstLate);
      Serial.println(" us late");
    }
  }
}
