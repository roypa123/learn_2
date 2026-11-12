// blink_millis.ino - blink WITHOUT delay(), so the loop can watch the button thousands of times a second
const int LED_PIN = 13;
const int BUTTON_PIN = 2;
const unsigned long HALF_PERIOD_MS = 500;   // the LED changes every 500 ms

unsigned long lastToggle = 0;          // when the LED last changed
bool ledOn = false;
int lastLevel = HIGH;
long presses = 0;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  if (millis() - lastToggle >= HALF_PERIOD_MS) {   // is it time to change the LED?
    lastToggle += HALF_PERIOD_MS;                  // the next change is due 500 ms after this one was due
    ledOn = !ledOn;                                // ! turns true into false and false into true
    digitalWrite(LED_PIN, ledOn);
  }

  int level = digitalRead(BUTTON_PIN);             // this line now runs on every pass
  if (lastLevel == HIGH && level == LOW) {
    presses++;
    Serial.print("press seen at ");
    Serial.print(millis());
    Serial.print(" ms, total ");
    Serial.println(presses);
  }
  lastLevel = level;
}
