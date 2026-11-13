// sensor_stream.ino - send a joint angle to the PC as lines of comma-separated text (CSV), 10 lines per second
const int ANGLE_PIN = A0;              // a 270-degree potentiometer on a joint (Chapter 101)
unsigned long lastSend = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("time_ms,angle_deg"); // a header line that names the columns
}

void loop() {
  if (millis() - lastSend >= 100) {
    lastSend += 100;
    int raw = analogRead(ANGLE_PIN);
    float angle = raw * 270.0 / 1023.0;
    Serial.print(millis());
    Serial.print(',');
    Serial.println(angle, 1);
  }
}
