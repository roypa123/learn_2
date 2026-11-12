// bumpers.ino - Rover's two bumpers, debounced; decide which way to turn after a bump
const int N = 2;
const int BUMPER_PIN[N] = {4, 7};      // [0] = left bumper, [1] = right bumper (switches to GND)
const unsigned long DEBOUNCE_MS = 5;

int lastReading[N] = {HIGH, HIGH};
unsigned long lastChange[N] = {0, 0};
int stableLevel[N] = {HIGH, HIGH};

// Debounce bumper i. Returns true only at the moment a new, real press is accepted.
bool newPress(int i) {
  int reading = digitalRead(BUMPER_PIN[i]);
  if (reading != lastReading[i]) {
    lastChange[i] = millis();
    lastReading[i] = reading;
  }
  if (millis() - lastChange[i] >= DEBOUNCE_MS && reading != stableLevel[i]) {
    stableLevel[i] = reading;
    return stableLevel[i] == LOW;      // true for a press, false for a release
  }
  return false;
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < N; i++) {
    pinMode(BUMPER_PIN[i], INPUT_PULLUP);
  }
}

void loop() {
  bool leftNew = newPress(0);
  bool rightNew = newPress(1);
  if (leftNew || rightNew) {
    bool left = stableLevel[0] == LOW;   // which bumpers are pressed right now?
    bool right = stableLevel[1] == LOW;
    Serial.print(millis());
    Serial.print(" ms: ");
    if (left && right) {
      Serial.println("both bumpers: back up, turn around");
    } else if (left) {
      Serial.println("left bumper: back up, turn right");
    } else {
      Serial.println("right bumper: back up, turn left");
    }
  }
}
