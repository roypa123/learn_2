// debounce_fsm.ino - Chapter 99's debounce, written as a small state machine with four states
const int BUTTON_PIN = 2;
const unsigned long DEBOUNCE_MS = 5;

enum ButtonState { UP, MAYBE_DOWN, DOWN, MAYBE_UP };
ButtonState bstate = UP;
unsigned long changeTime = 0;          // when we entered MAYBE_DOWN or MAYBE_UP
long presses = 0;
unsigned long lastReport = 0;

void updateButton() {
  int level = digitalRead(BUTTON_PIN);
  switch (bstate) {
    case UP:                                       // free, and believed free
      if (level == LOW) {
        bstate = MAYBE_DOWN;
        changeTime = millis();
      }
      break;
    case MAYBE_DOWN:                               // looks pressed: is it real?
      if (level == HIGH) {
        bstate = UP;                               // it was a bounce
      } else if (millis() - changeTime >= DEBOUNCE_MS) {
        bstate = DOWN;                             // steady for 5 ms: a real press
        presses++;
      }
      break;
    case DOWN:                                     // pressed, and believed pressed
      if (level == HIGH) {
        bstate = MAYBE_UP;
        changeTime = millis();
      }
      break;
    case MAYBE_UP:                                 // looks released: is it real?
      if (level == LOW) {
        bstate = DOWN;
      } else if (millis() - changeTime >= DEBOUNCE_MS) {
        bstate = UP;
      }
      break;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  updateButton();
  if (millis() - lastReport >= 1000) {
    lastReport += 1000;
    Serial.print("presses counted: ");
    Serial.println(presses);
  }
}
