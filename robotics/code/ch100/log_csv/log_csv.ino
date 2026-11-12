// log_csv.ino - log Rover's sensors 50 times a second as CSV lines: time, wheel speeds, battery, distance
const long BAUD = 9600;                // try 115200
const unsigned long PERIOD_MS = 20;    // one line every 20 ms = 50 lines per second

unsigned long nextLine = 0;            // when the next line is due

void setup() {
  Serial.begin(BAUD);
  Serial.println("time_ms,left_mm_s,right_mm_s,battery_mv,front_cm");
}

void loop() {
  if (millis() >= nextLine) {          // a line is due (or overdue)
    unsigned long now = millis();
    int left = 300 + (now / 7) % 11;   // pretend wheel speeds that change a little
    int right = 295 + (now / 5) % 13;
    int battery = 7412 - now / 1000;   // pretend battery millivolts, falling slowly
    int front = 150 - now / 100;       // pretend distance to a wall, getting closer
    Serial.print(now);
    Serial.print(",");
    Serial.print(left);
    Serial.print(",");
    Serial.print(right);
    Serial.print(",");
    Serial.print(battery);
    Serial.print(",");
    Serial.println(front);
    nextLine = nextLine + PERIOD_MS;   // the next line is due 20 ms after this one was DUE
  }
}
