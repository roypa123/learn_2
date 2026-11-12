// slow_poll.ino - a loop that does other work between readings can miss short presses
const int BUTTON_PIN = 2;
const unsigned long WORK_MS = 200;     // pretend the rest of the loop takes 200 ms (try 0)

int lastLevel = HIGH;
long seen = 0;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int level = digitalRead(BUTTON_PIN);  // the button is looked at only here, once per pass
  if (lastLevel == HIGH && level == LOW) {
    seen++;
    Serial.print(millis());
    Serial.print(" ms: press seen, total ");
    Serial.println(seen);
  }
  lastLevel = level;
  delay(WORK_MS);                       // everything else the robot does
}
