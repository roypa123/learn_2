// delay_blind.ino - blink with delay() and also watch a button: the button is looked at only once a second
const int LED_PIN = 13;
const int BUTTON_PIN = 2;

int lastLevel = HIGH;
long presses = 0;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(500);                          // for half a second the sketch does nothing else
  digitalWrite(LED_PIN, LOW);
  delay(500);                          // and again
  int level = digitalRead(BUTTON_PIN);
  if (lastLevel == HIGH && level == LOW) {
    presses++;
    Serial.print("press seen at ");
    Serial.print(millis());
    Serial.print(" ms, total ");
    Serial.println(presses);
  }
  lastLevel = level;
}
