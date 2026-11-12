// status_bumpers.ino - Rover's red "go home" light flashes 5 times a second WHILE the bumper is watched
// (Chapter 98's version used delay() and was blind while it flashed)
const int RED_PIN = 12;
const int BUMPER_PIN = 4;
const unsigned long FLASH_MS = 100;    // red: 100 ms on, 100 ms off

unsigned long lastFlash = 0;
bool redOn = false;
int lastLevel = HIGH;

void setup() {
  Serial.begin(115200);
  pinMode(RED_PIN, OUTPUT);
  pinMode(BUMPER_PIN, INPUT_PULLUP);
}

void loop() {
  if (millis() - lastFlash >= FLASH_MS) {          // job 1: the flashing light
    lastFlash += FLASH_MS;
    redOn = !redOn;
    digitalWrite(RED_PIN, redOn);
  }
  int level = digitalRead(BUMPER_PIN);              // job 2: the bumper, on every pass
  if (lastLevel == HIGH && level == LOW) {
    Serial.print("bump at ");
    Serial.print(micros() / 1000.0, 3);             // the time in ms, with microseconds
    Serial.println(" ms: motors stop");
  }
  lastLevel = level;
}
