// loop_delay.ino - a "100 Hz" control loop made with delay(10): how often does it really run?
const int SENSOR_PIN = A0;

long loops = 0;
int reading = 0;                       // the latest averaged sensor reading

void controlStep() {                   // the work of one control step: read the sensor 20 times (about 2.2 ms)
  long sum = 0;
  for (int i = 0; i < 20; i++) {
    sum += analogRead(SENSOR_PIN);
  }
  reading = sum / 20;
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  controlStep();
  loops++;
  if (loops % 100 == 0) {              // every 100 steps, say when they finished
    Serial.print(loops);
    Serial.print(" steps done at ");
    Serial.print(millis());
    Serial.println(" ms");
  }
  delay(10);                           // "wait 10 ms" - but the work above took time too
}
