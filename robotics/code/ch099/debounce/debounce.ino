// debounce.ino - count button presses, accepting a new level only after it has been steady for 5 ms
const int BUTTON_PIN = 2;
const unsigned long DEBOUNCE_MS = 5;

int lastReading = HIGH;                // the raw level on the previous pass
unsigned long lastChange = 0;          // when the raw level last changed
int stableLevel = HIGH;                // the debounced level: what we believe the button is doing
long presses = 0;
unsigned long lastReport = 0;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int reading = digitalRead(BUTTON_PIN);
  if (reading != lastReading) {        // the raw level moved: start timing again
    lastChange = millis();
    lastReading = reading;
  }
  if (millis() - lastChange >= DEBOUNCE_MS && reading != stableLevel) {
    stableLevel = reading;             // steady for 5 ms: accept the new level
    if (stableLevel == LOW) {
      presses++;                       // a real press (an edge of the debounced level)
    }
  }

  if (millis() - lastReport >= 1000) {
    lastReport = millis();
    Serial.print("presses counted: ");
    Serial.println(presses);
  }
}
