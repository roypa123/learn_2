// count_raw.ino - count button presses by watching for HIGH-to-LOW changes, with no debouncing
const int BUTTON_PIN = 2;

int lastLevel = HIGH;                  // the level on the previous pass of loop()
long presses = 0;
unsigned long lastReport = 0;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int level = digitalRead(BUTTON_PIN);
  if (lastLevel == HIGH && level == LOW) {   // it WAS free and IS now pressed: an edge
    presses++;
  }
  lastLevel = level;                   // remember this level for the next pass

  if (millis() - lastReport >= 1000) {
    lastReport = millis();
    Serial.print("presses counted: ");
    Serial.println(presses);
  }
}
