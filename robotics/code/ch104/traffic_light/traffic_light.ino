// traffic_light.ino - a traffic light as a state machine: each state has its own lights and its own time
const int RED_PIN = 10;
const int YELLOW_PIN = 11;
const int GREEN_PIN = 12;

enum Light { RED, GREEN, YELLOW };                 // the three states, as names
const char *NAMES[] = {"RED", "GREEN", "YELLOW"};  // their names as text, for printing
const unsigned long DURATION[] = {3000, 2500, 1000};   // how long each state lasts, in ms

Light state = RED;
unsigned long stateStart = 0;          // when we entered the current state

void enterState(Light next) {          // the only place where the state changes
  state = next;
  stateStart = millis();
  digitalWrite(RED_PIN, state == RED);           // entry action: show this state's lights
  digitalWrite(YELLOW_PIN, state == YELLOW);
  digitalWrite(GREEN_PIN, state == GREEN);
  Serial.print(millis());
  Serial.print(" ms: ");
  Serial.println(NAMES[state]);
}

void setup() {
  Serial.begin(115200);
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  enterState(RED);
}

void loop() {
  if (millis() - stateStart < DURATION[state]) {
    return;                            // not time to change yet: leave loop() at once
  }
  switch (state) {                     // time is up: which state comes next?
    case RED:
      enterState(GREEN);
      break;
    case GREEN:
      enterState(YELLOW);
      break;
    case YELLOW:
      enterState(RED);
      break;
  }
}
