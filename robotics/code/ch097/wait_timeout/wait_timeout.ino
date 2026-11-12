// wait_timeout.ino - wait for the start button, but never for ever
const int BUTTON_PIN = 2;
const unsigned long TIMEOUT_MS = 3000;

bool waitForButton(unsigned long timeoutMs) {
  unsigned long start = millis();
  while (digitalRead(BUTTON_PIN) == HIGH) {      // HIGH = not pressed (a pull-up, Chapter 83)
    if (millis() - start >= timeoutMs) {
      return false;                              // waited long enough: give up
    }
  }
  return true;                                   // the button was pressed
}

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.println("press the start button within 3 seconds");
  if (waitForButton(TIMEOUT_MS)) {
    Serial.print("started at ");
    Serial.print(millis());
    Serial.println(" ms");
  } else {
    Serial.println("no button: staying parked");
  }
}

void loop() {
}
