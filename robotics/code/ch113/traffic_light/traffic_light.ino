// traffic_light.ino - a pedestrian crossing: a state machine (Chapter 104) timed with millis() (Chapter 103),
// with a debounced request button from RoverLib (Chapter 110)
#include <Debouncer.h>

const int CAR_RED = 4;
const int CAR_YELLOW = 5;
const int CAR_GREEN = 6;
const int WALK_RED = 7;
const int WALK_GREEN = 8;
const int WAIT_LED = 13;               // "request received", the built-in LED
Debouncer button(12);                  // the pedestrians' button, pin 12 to GND

enum State { CARS_GO, CARS_SLOW, ALL_STOP, WALK, WALK_ENDING, CLEAR, CARS_READY };
const char *NAMES[] = {"CARS_GO", "CARS_SLOW", "ALL_STOP", "WALK", "WALK_ENDING", "CLEAR", "CARS_READY"};
const unsigned long MIN_GREEN_MS = 8000;   // cars always get at least this much green

State state = CARS_GO;
unsigned long enteredAt = 0;           // when the current state began
bool requested = false;

void lights(int cr, int cy, int cg, int wr, int wg) {
  digitalWrite(CAR_RED, cr);
  digitalWrite(CAR_YELLOW, cy);
  digitalWrite(CAR_GREEN, cg);
  digitalWrite(WALK_RED, wr);
  digitalWrite(WALK_GREEN, wg);
}

void enter(State s) {                  // every change of state goes through here
  state = s;
  enteredAt = millis();
  Serial.print(enteredAt);
  Serial.print(" ms: ");
  Serial.println(NAMES[s]);
  switch (s) {
    case CARS_GO:     lights(LOW, LOW, HIGH, HIGH, LOW); break;
    case CARS_SLOW:   lights(LOW, HIGH, LOW, HIGH, LOW); break;
    case ALL_STOP:    lights(HIGH, LOW, LOW, HIGH, LOW); break;
    case WALK:        lights(HIGH, LOW, LOW, LOW, HIGH);
                      requested = false;
                      digitalWrite(WAIT_LED, LOW);
                      break;
    case WALK_ENDING: break;             // the walk light flashes: see loop()
    case CLEAR:       lights(HIGH, LOW, LOW, HIGH, LOW); break;
    case CARS_READY:  lights(HIGH, HIGH, LOW, HIGH, LOW); break;
  }
}

void setup() {
  Serial.begin(115200);
  for (int pin = 4; pin <= 8; pin++) {
    pinMode(pin, OUTPUT);
  }
  pinMode(WAIT_LED, OUTPUT);
  button.begin();
  enter(CARS_GO);
}

void loop() {
  if (button.update() && !requested && state != WALK && state != WALK_ENDING) {
    requested = true;
    digitalWrite(WAIT_LED, HIGH);
    Serial.print(millis());
    Serial.println(" ms: button pressed, request noted");
  }
  unsigned long t = millis() - enteredAt;
  switch (state) {
    case CARS_GO:
      if (requested && t >= MIN_GREEN_MS) enter(CARS_SLOW);
      break;
    case CARS_SLOW:
      if (t >= 3000) enter(ALL_STOP);
      break;
    case ALL_STOP:
      if (t >= 1000) enter(WALK);
      break;
    case WALK:
      if (t >= 6000) enter(WALK_ENDING);
      break;
    case WALK_ENDING:
      digitalWrite(WALK_GREEN, (t / 250) % 2 == 0 ? HIGH : LOW);   // flash at 2 Hz: hurry up
      if (t >= 4000) enter(CLEAR);
      break;
    case CLEAR:
      if (t >= 2000) enter(CARS_READY);
      break;
    case CARS_READY:
      if (t >= 1500) enter(CARS_GO);
      break;
  }
}
