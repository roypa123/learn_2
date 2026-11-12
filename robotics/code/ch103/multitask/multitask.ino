// multitask.ino - three jobs at three different rates in one loop, and none of them ever waits
const int LED_PIN = 13;
const int SENSOR_PIN = A0;
const unsigned long BLINK_MS = 250;    // job 1: change the LED every 250 ms (2 blinks a second)
const unsigned long SENSOR_MS = 100;   // job 2: read the sensor every 100 ms
const unsigned long REPORT_MS = 1000;  // job 3: report once a second

unsigned long lastBlink = 0;
unsigned long lastSensor = 0;
unsigned long lastReport = 0;
bool ledOn = false;
long sensorSum = 0;                    // readings added up since the last report
int sensorCount = 0;
long passes = 0;                       // passes of loop() since the last report

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  passes++;
  if (millis() - lastBlink >= BLINK_MS) {          // job 1
    lastBlink += BLINK_MS;
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn);
  }
  if (millis() - lastSensor >= SENSOR_MS) {        // job 2
    lastSensor += SENSOR_MS;
    sensorSum += analogRead(SENSOR_PIN);
    sensorCount++;
  }
  if (millis() - lastReport >= REPORT_MS) {        // job 3
    lastReport += REPORT_MS;
    Serial.print(millis() / 1000);
    Serial.print(" s: ");
    Serial.print(sensorCount);
    Serial.print(" readings, average ");
    Serial.print(sensorSum / sensorCount);
    Serial.print(", loop ran ");
    Serial.print(passes);
    Serial.println(" times");
    sensorSum = 0;
    sensorCount = 0;
    passes = 0;
  }
}
