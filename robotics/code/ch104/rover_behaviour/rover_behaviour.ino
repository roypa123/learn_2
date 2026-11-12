// rover_behaviour.ino - Rover's first behaviour as a state machine:
// wait for the start button, drive, and after a bump: back up, then turn away from the side that was hit
const int N = 3;
const int PIN[N] = {2, 4, 7};          // [0] start button, [1] left bumper, [2] right bumper (all to GND)
const unsigned long DEBOUNCE_MS = 5;
const unsigned long BACK_UP_MS = 500;
const unsigned long TURN_MS = 400;     // a 90-degree turn; turning around takes twice as long

enum State { WAIT_START, DRIVE, BACK_UP, TURN_LEFT, TURN_RIGHT, TURN_AROUND };
const char *NAMES[] = {"WAIT_START", "DRIVE", "BACK_UP", "TURN_LEFT", "TURN_RIGHT", "TURN_AROUND"};
const char *MOTORS[] = {"stop", "forward", "backward", "spin left", "spin right", "spin right"};

State state = WAIT_START;
unsigned long stateStart = 0;
bool leftHit = false;                  // which bumpers were hit during this bump
bool rightHit = false;

int lastReading[N] = {HIGH, HIGH, HIGH};
unsigned long lastChange[N] = {0, 0, 0};
int stableLevel[N] = {HIGH, HIGH, HIGH};

bool newPress(int i) {                 // Chapter 99's debounce: true only at the moment of a real press
  int reading = digitalRead(PIN[i]);
  if (reading != lastReading[i]) {
    lastChange[i] = millis();
    lastReading[i] = reading;
  }
  if (millis() - lastChange[i] >= DEBOUNCE_MS && reading != stableLevel[i]) {
    stableLevel[i] = reading;
    return stableLevel[i] == LOW;
  }
  return false;
}

void enterState(State next) {
  state = next;
  stateStart = millis();
  Serial.print(millis());
  Serial.print(" ms: ");
  Serial.print(NAMES[state]);
  Serial.print("   motors: ");
  Serial.println(MOTORS[state]);
}

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < N; i++) {
    pinMode(PIN[i], INPUT_PULLUP);
  }
  enterState(WAIT_START);
}

void loop() {
  bool startNew = newPress(0);         // check every input on every pass (Chapter 99)
  bool leftNew = newPress(1);
  bool rightNew = newPress(2);
  unsigned long inState = millis() - stateStart;

  if (startNew && state != WAIT_START) {   // in ANY moving state, the start button means "stop now"
    enterState(WAIT_START);
    return;
  }

  switch (state) {
    case WAIT_START:
      if (startNew) {
        enterState(DRIVE);
      }
      break;
    case DRIVE:
      if (leftNew || rightNew) {
        leftHit = leftNew;
        rightHit = rightNew;
        enterState(BACK_UP);
      }
      break;
    case BACK_UP:
      if (leftNew) {
        leftHit = true;                // the other bumper may close a moment later
      }
      if (rightNew) {
        rightHit = true;
      }
      if (inState >= BACK_UP_MS) {
        if (leftHit && rightHit) {
          enterState(TURN_AROUND);
        } else if (leftHit) {
          enterState(TURN_RIGHT);      // hit on the left: turn away, to the right
        } else {
          enterState(TURN_LEFT);
        }
      }
      break;
    case TURN_LEFT:
    case TURN_RIGHT:
      if (inState >= TURN_MS) {
        enterState(DRIVE);
      }
      break;
    case TURN_AROUND:
      if (inState >= 2 * TURN_MS) {
        enterState(DRIVE);
      }
      break;
  }
}
